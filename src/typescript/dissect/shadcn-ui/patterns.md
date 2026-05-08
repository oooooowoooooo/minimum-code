# shadcn/ui — Core Design Patterns

## Pattern 1: Copy-Paste Ownership

### What It Is
Instead of `npm install`, you run `npx shadcn add button`. This copies the component source into your project.

### Why It's Better
1. **No version drift** — you control when to update
2. **Full customization** — modify any component freely
3. **No lock-in** — remove shadcn anytime, code stays yours
4. **Learning** — read the source, understand the pattern

---

## Pattern 2: Variant System (CVA)

### What It Is
`class-variance-authority` (CVA) maps props to Tailwind classes. One component, many visual variants.

```typescript
const buttonVariants = cva("base-classes", {
  variants: {
    variant: {
      default: "bg-primary text-white",
      outline: "border border-input bg-transparent",
      ghost: "hover:bg-accent",
    },
    size: {
      default: "h-10 px-4",
      sm: "h-9 px-3",
      lg: "h-11 px-8",
    },
  },
  defaultVariants: { variant: "default", size: "default" },
});
```

### Why It Works
1. **Type-safe** — invalid variants caught at compile time
2. **Composable** — combine variant + size freely
3. **Tree-shakeable** — unused variants eliminated in build

---

## Pattern 3: The Slot Pattern (asChild)

### What It Is
Radix's `asChild` merges a component's behavior onto its child instead of rendering a wrapper.

```tsx
// Without asChild: <button><a>Click</a></button>  ← invalid HTML
// With asChild:    <a>Click</a>                    ← button behavior on <a>
<DialogTrigger asChild>
  <a href="/open">Open Dialog</a>
</DialogTrigger>
```

### Why It Matters
1. **Semantic HTML** — render the right element for the context
2. **Styling freedom** — style the child, not the wrapper
3. **Composability** — combine primitives without DOM nesting

---

## Pattern 4: CSS Variables Theming

### What It Is
All colors reference CSS variables. Change the variables = change the entire theme.

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
}
.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

### Why It Works
1. **One file** controls the entire app's look
2. **Dark mode** is just swapping variable values
3. **User themes** — let users set their own colors
4. **No rebuild** — CSS variables update at runtime

---

## Pattern 5: Composition Over Configuration

### What It Is
Instead of a `<Form>` component with 50 props, compose smaller pieces:

```tsx
<Form>
  <FormField name="email">
    <FormLabel>Email</FormLabel>
    <FormControl>
      <Input type="email" />
    </FormControl>
    <FormMessage />
  </FormField>
</Form>
```

### Why It Works
1. **Each piece is simple** — easy to understand and modify
2. **Flexible** — rearrange, add, or remove pieces freely
3. **No magic** — explicit composition, no hidden behavior

---

## Key Takeaways

1. **Own your components** — copy, don't install
2. **CVA variants** — type-safe style variations from one component
3. **asChild slot** — polymorphic components without wrapper hell
4. **CSS variables** — theming without JavaScript
5. **Composition** — small pieces > monolithic components
6. **Radix primitives** — accessibility is a solved problem
