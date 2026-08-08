import { describe, expect, it } from 'vitest';
import { routeForPath, workbenchRoutes } from './routes';

describe('routeForPath', () => {
  it.each([
    ['/', 'import'],
    ['/import', 'import'],
    ['/mapping', 'mapping'],
    ['/mapping/concept-1', 'mapping'],
    ['/learning', 'learning'],
    ['/review', 'review'],
    ['/settings', 'settings'],
  ])('classifies %s as %s', (pathname, expectedId) => {
    expect(routeForPath(pathname).id).toBe(expectedId);
  });

  it.each(['/imported', '/mappingfoo', '/unknown'])('fails closed for %s', (pathname) => {
    expect(routeForPath(pathname)).toEqual({ id: 'not-found', pathname });
  });

  it('keeps utility and unavailable routes out of the four-stage workflow navigation', () => {
    expect(workbenchRoutes.map(({ id }) => id)).toEqual([
      'import',
      'mapping',
      'learning',
      'review',
    ]);
    expect(workbenchRoutes.every((route) => !('icon' in route))).toBe(true);
  });
});
