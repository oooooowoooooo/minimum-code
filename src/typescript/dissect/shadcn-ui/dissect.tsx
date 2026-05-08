/**
 * shadcn/ui — Atomic Code Dissection
 * ====================================
 * Simplified implementations of shadcn/ui's core patterns.
 * Demonstrates variant system, composition, and theming.
 *
 * Note: This file uses JSX syntax. Run with a React-aware tool.
 */

// ============================================================================
// SECTION 1: VARIANT SYSTEM (CVA-like)
// ============================================================================
// How one component supports multiple visual styles via props.

type VariantConfig = Record<string, Record<string, string>>;

interface CVAOptions {
  base: string;
  variants: VariantConfig;
  defaultVariants?: Record<string, string>;
}

/**
 * Simplified class-variance-authority (CVA).
 * Maps variant props to Tailwind class strings.
 */
function cva(options: CVAOptions) {
  return (props: Record<string, string | undefined> = {}): string => {
    const classes = [options.base];

    for (const [variantKey, variantMap] of Object.entries(options.variants)) {
      const value = props[variantKey]
        ?? options.defaultVariants?.[variantKey]
        ?? Object.keys(variantMap)[0];
      if (value && variantMap[value]) {
        classes.push(variantMap[value]);
      }
    }

    return classes.filter(Boolean).join(' ');
  };
}

// Test
console.log('=== Variant System (CVA) ===');

const buttonVariants = cva({
  base: 'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  variants: {
    variant: {
      default: 'bg-blue-600 text-white hover:bg-blue-700',
      outline: 'border border-gray-300 bg-transparent hover:bg-gray-100',
      ghost: 'hover:bg-gray-100',
      destructive: 'bg-red-600 text-white hover:bg-red-700',
    },
    size: {
      sm: 'h-9 px-3 text-sm',
      default: 'h-10 px-4',
      lg: 'h-11 px-8 text-lg',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'default',
  },
});

console.log('Default:', buttonVariants());
console.log('Outline SM:', buttonVariants({ variant: 'outline', size: 'sm' }));
console.log('Destructive LG:', buttonVariants({ variant: 'destructive', size: 'lg' }));


// ============================================================================
// SECTION 2: MERGE CLASSNAMES (cn utility)
// ============================================================================
// How shadcn/ui merges Tailwind classes without conflicts.

/**
 * Simplified tailwind-merge + clsx.
 * Merges class strings, deduplicates, handles conflicts.
 */
function cn(...inputs: (string | undefined | null | false)[]): string {
  return inputs.filter(Boolean).join(' ');
}

// Test
console.log('\n=== Class Merging ===');
console.log(cn('px-4 py-2', 'px-6'));           // px-4 py-2 px-6 (simplified)
console.log(cn('bg-red-500', undefined, 'text-white')); // bg-red-500 text-white


// ============================================================================
// SECTION 3: COMPOSITION PATTERN
// ============================================================================
// How complex components are built from small, composable pieces.

interface ComponentProps {
  children?: any;
  className?: string;
  [key: string]: any;
}

/**
 * Simplified component composition.
 * Each piece is a function that returns a description of what to render.
 */

function Form({ children, className }: ComponentProps) {
  return { type: 'form', className: cn('space-y-4', className), children };
}

function FormField({ name, children }: { name: string; children: any }) {
  return { type: 'field', name, children };
}

function FormLabel({ children, className }: ComponentProps) {
  return { type: 'label', className: cn('text-sm font-medium', className), children };
}

function FormControl({ children }: { children: any }) {
  return { type: 'control', children };
}

function FormMessage({ children }: { children?: string }) {
  return { type: 'message', className: 'text-sm text-red-500', children };
}

// Test
console.log('\n=== Composition Pattern ===');
const form = Form({
  children: [
    FormField({
      name: 'email',
      children: [
        FormLabel({ children: 'Email Address' }),
        FormControl({ children: '<input type="email" />' }),
        FormMessage({ children: 'Please enter a valid email' }),
      ],
    }),
  ],
});
console.log('Form structure:', JSON.stringify(form, null, 2));


// ============================================================================
// SECTION 4: CSS VARIABLES THEMING
// ============================================================================
// How one config file controls the entire app's look.

interface Theme {
  name: string;
  variables: Record<string, string>;
}

const lightTheme: Theme = {
  name: 'light',
  variables: {
    '--background': '0 0% 100%',
    '--foreground': '222.2 84% 4.9%',
    '--primary': '222.2 47.4% 11.2%',
    '--primary-foreground': '210 40% 98%',
    '--muted': '210 40% 96.1%',
    '--border': '214.3 31.8% 91.4%',
  },
};

const darkTheme: Theme = {
  name: 'dark',
  variables: {
    '--background': '222.2 84% 4.9%',
    '--foreground': '210 40% 98%',
    '--primary': '210 40% 98%',
    '--primary-foreground': '222.2 47.4% 11.2%',
    '--muted': '217.2 32.6% 17.5%',
    '--border': '217.2 32.6% 17.5%',
  },
};

function applyTheme(theme: Theme): string {
  return `:root {\n${
    Object.entries(theme.variables)
      .map(([key, value]) => `  ${key}: ${value};`)
      .join('\n')
  }\n}`;
}

// Test
console.log('\n=== CSS Variables Theming ===');
console.log('Light theme CSS:');
console.log(applyTheme(lightTheme));
console.log('\nDark theme CSS:');
console.log(applyTheme(darkTheme));


// ============================================================================
// SECTION 5: asChild PATTERN (Slot)
// ============================================================================
// How Radix merges component behavior onto a child element.

interface AsChildProps {
  asChild?: boolean;
  children: any;
}

/**
 * Simplified asChild implementation.
 * When asChild=true, the component's props merge onto the child.
 */
function Slot({ children, ...props }: Record<string, any>) {
  // In real Radix, this clones the child element and merges props
  return {
    type: 'slot',
    mergedProps: props,
    child: children,
  };
}

function Trigger({ asChild, children, ...props }: AsChildProps) {
  if (asChild) {
    return Slot({ children, ...props });
  }
  return { type: 'button', ...props, children };
}

// Test
console.log('\n=== asChild Pattern ===');

// Without asChild: renders a button
const defaultTrigger = Trigger({ children: 'Click me' });
console.log('Default trigger:', defaultTrigger);

// With asChild: merges onto child
const customTrigger = Trigger({
  asChild: true,
  children: { type: 'a', href: '/open', children: 'Open Dialog' },
});
console.log('Custom trigger (asChild):', customTrigger);


// ============================================================================
// SECTION 6: COMPONENT REGISTRY
// ============================================================================
// How shadcn/ui manages which components are installed.

interface ComponentEntry {
  name: string;
  path: string;
  dependencies: string[];
  installed: boolean;
}

class ComponentRegistry {
  private components: Map<string, ComponentEntry> = new Map();

  register(name: string, dependencies: string[] = []): void {
    this.components.set(name, {
      name,
      path: `components/ui/${name}.tsx`,
      dependencies,
      installed: false,
    });
  }

  /**
   * Install a component and its dependencies.
   */
  install(name: string): string[] {
    const entry = this.components.get(name);
    if (!entry) throw new Error(`Component "${name}" not found`);

    const installed: string[] = [];

    // Install dependencies first
    for (const dep of entry.dependencies) {
      const depEntry = this.components.get(dep);
      if (depEntry && !depEntry.installed) {
        depEntry.installed = true;
        installed.push(dep);
      }
    }

    entry.installed = true;
    installed.push(name);
    return installed;
  }

  listInstalled(): string[] {
    return [...this.components.values()]
      .filter(c => c.installed)
      .map(c => c.name);
  }
}

// Test
console.log('\n=== Component Registry ===');
const registry = new ComponentRegistry();
registry.register('button');
registry.register('input');
registry.register('label');
registry.register('form', ['button', 'input', 'label']);
registry.register('dialog', ['button']);
registry.register('dropdown-menu', ['dialog', 'button']);

const installed = registry.install('dropdown-menu');
console.log('Installed:', installed);
console.log('All installed:', registry.listInstalled());


// ============================================================================
// KEY TAKEAWAYS
// ============================================================================
/*
1. CVA variants — one component, many styles, type-safe
2. cn() utility — merge Tailwind classes without conflicts
3. Composition — small pieces combine into complex UIs
4. CSS variables theming — one file controls the entire look
5. asChild/Slot — polymorphic components without wrapper hell
6. Component registry — manage installation and dependencies
7. OWN your components — copy, don't install from npm
*/
