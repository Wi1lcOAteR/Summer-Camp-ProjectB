import type { LucideIcon } from 'lucide-react';
import { BookOpenCheck, CalendarRange, FileInput, Network } from 'lucide-react';

export interface WorkbenchRoute {
  href: string;
  label: string;
  detail: string;
  icon: LucideIcon;
}

export const workbenchRoutes: readonly WorkbenchRoute[] = [
  { href: '/import', label: '导入', detail: '导入材料', icon: FileInput },
  { href: '/mapping', label: '映射', detail: '确认映射', icon: Network },
  { href: '/learning', label: '学习', detail: '练习与掌握', icon: BookOpenCheck },
  { href: '/review', label: '复习', detail: '复习计划', icon: CalendarRange },
];

export function routeForPath(pathname: string): WorkbenchRoute {
  return workbenchRoutes.find(({ href }) => pathname.startsWith(href)) ?? workbenchRoutes[2]!;
}
