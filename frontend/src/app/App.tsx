import { createRoot } from 'react-dom/client';
import { LockKeyhole, Settings } from 'lucide-react';
import { routeForPath, workbenchRoutes, type RouteMatch, type WorkbenchRouteId } from './routes';
import { ImportView } from '../views/import/ImportView';
import { LearningView } from '../views/learning/LearningView';
import { MappingView } from '../views/mapping/MappingView';
import { ReviewView } from '../views/review/ReviewView';
import '../styles/global.css';

export function App() {
  const path = typeof window === 'undefined' ? '/import' : window.location.pathname;
  const current = routeForPath(path);
  return (
    <div className="shell">
      <header className="shellHeader">
        <div className="utilityBar">
          <div className="brand">
            <span className="brandMark" aria-hidden="true">PB</span>
            <div>
              <p className="brandName">ProjectB</p>
              <p className="brandContext">{'\u672c\u5730\u5b66\u4e60\u5de5\u4f5c\u53f0'}</p>
            </div>
          </div>
          <div className="course"><span>{'\u8bfe\u7a0b'}</span><strong>{'\u64cd\u4f5c\u7cfb\u7edf'}</strong></div>
          <div className="utilityStatus" aria-label={'\u8fd0\u884c\u72b6\u6001'}>
            <span className="statusPill"><LockKeyhole size={15} aria-hidden="true" />{'\u4ec5\u672c\u673a'}</span>
            <span className="statusPill"><span className="statusDot" aria-hidden="true" />{'\u672c\u5730\u6863\u6848\u6b63\u5e38'}</span>
          </div>
        </div>
        <nav className="workflow" aria-label={'\u5b66\u4e60\u6d41\u7a0b'}>
          <div className="workflowInner">
            <ol className="workflowList">
              {workbenchRoutes.map((route, index) => (
                <li key={route.id}>
                  <a className="stageLink" href={route.href} aria-label={route.label} aria-current={current.id === route.id ? 'page' : undefined}>
                    <span className="stageNumber" aria-hidden="true">{index + 1}</span>
                    <span className="stageCopy"><span className="stageLabel">{route.label}</span><span className="stageDetail">{route.detail}</span></span>
                  </a>
                </li>
              ))}
            </ol>
            <a className="settingsLink" href="/settings" title={'\u8bbe\u7f6e'} aria-current={current.id === 'settings' ? 'page' : undefined}>
              <Settings size={18} aria-hidden="true" /><span>{'\u8bbe\u7f6e'}</span>
            </a>
          </div>
        </nav>
      </header>
      <main>
        <div className="mainInner"><RouteContent route={current} /></div>
      </main>
    </div>
  );
}

function RouteContent({ route }: { route: RouteMatch }) {
  if (route.id === 'import') return <ImportView />;
  if (route.id === 'mapping') return <MappingView />;
  if (route.id === 'learning') return <LearningView />;
  if (route.id === 'review') return <ReviewView />;
  if (route.id === 'not-found') return <NotFoundView />;
  return <UnavailableView routeId={route.id} />;
}

const unavailableLabels: Record<Exclude<WorkbenchRouteId, 'import' | 'mapping' | 'learning' | 'not-found'>, string> = {
  review: '\u590d\u4e60',
  settings: '\u8bbe\u7f6e',
};

function UnavailableView({ routeId }: { routeId: keyof typeof unavailableLabels }) {
  const label = unavailableLabels[routeId];
  return (
    <section className="pageIntro" aria-labelledby="page-title">
      <div>
        <p className="eyebrow">{'\u5f53\u524d\u9636\u6bb5'}</p>
        <h1 id="page-title">{label}{'\u529f\u80fd\u6682\u4e0d\u53ef\u7528'}</h1>
        <p className="introCopy">{'\u8be5\u9875\u9762\u5c1a\u672a\u542f\u7528\u3002'}</p>
      </div>
    </section>
  );
}

function NotFoundView() {
  return (
    <section className="pageIntro" aria-labelledby="page-title">
      <div>
        <p className="eyebrow">404</p>
        <h1 id="page-title">{'\u9875\u9762\u4e0d\u5b58\u5728'}</h1>
      </div>
    </section>
  );
}

const rootElement = typeof document === 'undefined' ? null : document.getElementById('root');
if (rootElement) createRoot(rootElement).render(<App />);
