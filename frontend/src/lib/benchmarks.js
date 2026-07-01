function toKebabCase(name) {
    return name
        .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
        .toLowerCase();
}

const modules = import.meta.glob("../benchmarks/*.svelte", { eager: true });

const registry = {};
for (const path in modules) {
    const fileName = path.split("/").pop().replace(".svelte", "");
    const slug = toKebabCase(fileName);
    registry[slug] = modules[path].default;
}

export const BENCHMARKS = Object.keys(registry);

export function getBenchmarkComponent(slug) {
    return registry[slug];
}
