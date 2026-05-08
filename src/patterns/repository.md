# Repository

## What It Is

The Repository pattern mediates between the domain layer and data storage. It provides a collection-like
interface for accessing domain objects (entities), abstracting away the details of how data is stored,
queried, or persisted. The rest of the application works with repositories as if they were in-memory
collections, regardless of whether the underlying storage is PostgreSQL, MongoDB, a REST API, or a file.

## Why It Matters in the AI Era

AI applications have diverse storage needs: embeddings in a vector database, conversation history in
PostgreSQL, cached responses in Redis, training data in S3. The Repository pattern lets your business
logic (prompt construction, chain orchestration, result aggregation) work against a clean interface
without knowing which database is backing each data type. Swap Pinecone for pgvector? Change one
repository implementation. Add caching? Wrap the existing repository with a caching decorator.

## Python Example

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Conversation:
    id: str
    user_id: str
    messages: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class ConversationRepository(ABC):
    @abstractmethod
    def get_by_id(self, conversation_id: str) -> Optional[Conversation]: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> list[Conversation]: ...

    @abstractmethod
    def save(self, conversation: Conversation) -> None: ...

    @abstractmethod
    def delete(self, conversation_id: str) -> None: ...

    @abstractmethod
    def exists(self, conversation_id: str) -> bool: ...


class InMemoryConversationRepository(ConversationRepository):
    """For testing and development."""
    def __init__(self):
        self._store: dict[str, Conversation] = {}

    def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        return self._store.get(conversation_id)

    def get_by_user(self, user_id: str) -> list[Conversation]:
        return [c for c in self._store.values() if c.user_id == user_id]

    def save(self, conversation: Conversation) -> None:
        self._store[conversation.id] = conversation

    def delete(self, conversation_id: str) -> None:
        self._store.pop(conversation_id, None)

    def exists(self, conversation_id: str) -> bool:
        return conversation_id in self._store


class PostgresConversationRepository(ConversationRepository):
    """For production -- would use psycopg2 or asyncpg."""
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        # SQL: SELECT * FROM conversations WHERE id = %s
        raise NotImplementedError

    def get_by_user(self, user_id: str) -> list[Conversation]:
        # SQL: SELECT * FROM conversations WHERE user_id = %s
        raise NotImplementedError

    def save(self, conversation: Conversation) -> None:
        # SQL: INSERT ... ON CONFLICT UPDATE
        raise NotImplementedError

    def delete(self, conversation_id: str) -> None:
        # SQL: DELETE FROM conversations WHERE id = %s
        raise NotImplementedError

    def exists(self, conversation_id: str) -> bool:
        # SQL: SELECT EXISTS(SELECT 1 FROM conversations WHERE id = %s)
        raise NotImplementedError


# Business logic uses the interface, not the implementation
class ChatService:
    def __init__(self, repo: ConversationRepository):
        self.repo = repo

    def send_message(self, conversation_id: str, user_id: str, message: str) -> str:
        if not self.repo.exists(conversation_id):
            conversation = Conversation(
                id=conversation_id,
                user_id=user_id,
                messages=[{"role": "user", "content": message}],
            )
        else:
            conversation = self.repo.get_by_id(conversation_id)
            conversation.messages.append({"role": "user", "content": message})

        response = f"AI response to: {message}"
        conversation.messages.append({"role": "assistant", "content": response})
        self.repo.save(conversation)
        return response
```

## TypeScript Example

```typescript
interface Conversation {
  id: string;
  userId: string;
  messages: { role: string; content: string }[];
  createdAt: Date;
  metadata: Record<string, unknown>;
}

interface ConversationRepository {
  getById(id: string): Promise<Conversation | null>;
  getByUser(userId: string): Promise<Conversation[]>;
  save(conversation: Conversation): Promise<void>;
  delete(id: string): Promise<void>;
  exists(id: string): Promise<boolean>;
}

class InMemoryConversationRepository implements ConversationRepository {
  private store = new Map<string, Conversation>();

  async getById(id: string): Promise<Conversation | null> {
    return this.store.get(id) ?? null;
  }

  async getByUser(userId: string): Promise<Conversation[]> {
    return [...this.store.values()].filter((c) => c.userId === userId);
  }

  async save(conversation: Conversation): Promise<void> {
    this.store.set(conversation.id, { ...conversation });
  }

  async delete(id: string): Promise<void> {
    this.store.delete(id);
  }

  async exists(id: string): Promise<boolean> {
    return this.store.has(id);
  }
}

class PostgresConversationRepository implements ConversationRepository {
  constructor(private connectionString: string) {}

  async getById(id: string): Promise<Conversation | null> {
    // SQL query here
    throw new Error("Not implemented");
  }

  async getByUser(userId: string): Promise<Conversation[]> {
    throw new Error("Not implemented");
  }

  async save(conversation: Conversation): Promise<void> {
    throw new Error("Not implemented");
  }

  async delete(id: string): Promise<void> {
    throw new Error("Not implemented");
  }

  async exists(id: string): Promise<boolean> {
    throw new Error("Not implemented");
  }
}

// Business logic depends only on the interface
class ChatService {
  constructor(private repo: ConversationRepository) {}

  async sendMessage(
    conversationId: string,
    userId: string,
    message: string,
  ): Promise<string> {
    let conversation = await this.repo.getById(conversationId);
    if (!conversation) {
      conversation = {
        id: conversationId,
        userId,
        messages: [{ role: "user", content: message }],
        createdAt: new Date(),
        metadata: {},
      };
    } else {
      conversation.messages.push({ role: "user", content: message });
    }

    const response = `AI response to: ${message}`;
    conversation.messages.push({ role: "assistant", content: response });
    await this.repo.save(conversation);
    return response;
  }
}
```

## Where You'll See It

| Project | How Repository Appears |
|---------|----------------------|
| **Django** | `Model.objects` is a repository -- `filter()`, `get()`, `create()` abstract the SQL. |
| **TypeORM / Prisma** | `Repository<T>` with `find()`, `save()`, `delete()` methods maps to database tables. |
| **Spring Data JPA** | `JpaRepository<Entity, ID>` auto-generates repository implementations from interfaces. |
| **Clean Architecture repos** | The pattern is a core building block of Hexagonal / Clean Architecture. |
| **LangChain memory** | `BaseChatMessageHistory` is a repository for conversation history. |

## Mini-Exercises

1. **Caching decorator**: Write a `CachingConversationRepository` that wraps another repository.
   It caches `getById` results in a dict with a 5-minute TTL. Falls through to the inner repo on cache miss.

2. **Search method**: Add `search(query: str) -> list[Conversation]` to the repository interface.
   Implement it for in-memory (simple substring match) and describe how you would implement it for Postgres.

3. **Unit of work**: The repository pattern pairs well with Unit of Work (save multiple entities in one
   transaction). Design a `UnitOfWork` that collects changes across multiple repositories and commits
   them atomically.

## Key Takeaways

- Repository abstracts data access behind a clean interface that looks like an in-memory collection.
- Business logic depends on the interface, not the storage implementation -- enabling easy swaps and testing.
- In-memory implementations are ideal for unit tests; real implementations handle production storage.
- In AI applications, repositories manage conversations, embeddings, prompts, and user data across diverse stores.
- The pattern is the foundation of Clean Architecture and Domain-Driven Design.
