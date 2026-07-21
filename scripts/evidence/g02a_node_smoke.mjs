const modules = [
  "react",
  "react-dom",
  "lucide-react",
  "vite",
  "@vitejs/plugin-react",
  "typescript",
  "vitest",
  "@testing-library/react",
  "@testing-library/dom",
  "@testing-library/user-event",
  "jsdom",
  "@playwright/test",
  "@axe-core/playwright",
];

if (process.version !== "v24.18.0") {
  throw new Error(`Expected Node v24.18.0, observed ${process.version}`);
}

await Promise.all(modules.map((moduleName) => import(moduleName)));
const { getByRole } = await import("@testing-library/dom");
const { JSDOM } = await import("jsdom");
const document = new JSDOM("<button>Continue</button>").window.document;
if (getByRole(document.body, "button", { name: "Continue" }).textContent !== "Continue") {
  throw new Error("JSDOM role-query smoke failed");
}

console.log("NODE_SMOKE_PASS modules=13 jsdom_role_query=pass node=v24.18.0");
