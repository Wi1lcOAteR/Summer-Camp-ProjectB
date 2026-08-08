export type WorkbenchRouteId =
  | 'import'
  | 'mapping'
  | 'learning'
  | 'review'
  | 'settings'
  | 'not-found';

export interface WorkbenchRoute {
  id: Exclude<WorkbenchRouteId, 'not-found'>;
  href: string;
  label: string;
  detail: string;
  navigation: 'workflow' | 'utility';
}

export interface NotFoundRoute {
  id: 'not-found';
  pathname: string;
}

export type RouteMatch = WorkbenchRoute | NotFoundRoute;

export const routeRegistry: readonly WorkbenchRoute[] = [
  { id: 'import', href: '/import', label: '\u5bfc\u5165', detail: '\u5bfc\u5165\u6750\u6599', navigation: 'workflow' },
  { id: 'mapping', href: '/mapping', label: '\u6620\u5c04', detail: '\u786e\u8ba4\u6620\u5c04', navigation: 'workflow' },
  { id: 'learning', href: '/learning', label: '\u5b66\u4e60', detail: '\u7ec3\u4e60\u4e0e\u638c\u63e1', navigation: 'workflow' },
  { id: 'review', href: '/review', label: '\u590d\u4e60', detail: '\u590d\u4e60\u8ba1\u5212', navigation: 'workflow' },
  { id: 'settings', href: '/settings', label: '\u8bbe\u7f6e', detail: '\u672c\u5730\u914d\u7f6e', navigation: 'utility' },
];

export const workbenchRoutes = routeRegistry.filter(
  (route) => route.navigation === 'workflow',
);

export function routeForPath(pathname: string): RouteMatch {
  if (pathname === '/') return routeRegistry[0]!;
  const route = routeRegistry.find(
    ({ href }) => pathname === href || pathname.startsWith(`${href}/`),
  );
  return route ?? { id: 'not-found', pathname };
}
