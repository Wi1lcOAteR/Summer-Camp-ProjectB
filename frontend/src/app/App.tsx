import { createRoot } from 'react-dom/client';
import { LockKeyhole, Settings } from 'lucide-react';
import { useEffect, useState } from 'react';
import { routeForPath, workbenchRoutes, type RouteMatch } from './routes';
import { createApiClient, type ApiClient } from '../api/client';
import type { ApiCapabilities } from '../api/capabilities';
import { ImportView } from '../views/import/ImportView';
import { LearningView } from '../views/learning/LearningView';
import { MappingView } from '../views/mapping/MappingView';
import { ReviewView } from '../views/review/ReviewView';
import { SettingsView } from '../views/settings/SettingsView';
import '../styles/global.css';

const defaultApi = createApiClient();

export function App({ api = defaultApi }: { api?: Pick<ApiClient, 'getCapabilities'> }) {
  const [capabilities, setCapabilities] = useState<ApiCapabilities | undefined>();
  useEffect(() => {
    let active = true;
    void api.getCapabilities()
      .then((next) => { if (active) setCapabilities(next); })
      .catch(() => { if (active) setCapabilities(undefined); });
    return () => { active = false; };
  }, [api]);

  const path = typeof window === 'undefined' ? '/import' : window.location.pathname;
  const current = routeForPath(path);
  const isDemo = capabilities?.profile === 'demo';
  const isLocal = capabilities?.profile === 'local';
  return (
    <div className="shell">
      <header className="shellHeader">
        <div className="utilityBar">
          <div className="brand">
            <span className="brandMark" aria-hidden="true">PB</span>
            <div>
              <p className="brandName">ProjectB</p>
              <p className="brandContext">{isDemo ? 'Public demo workbench' : isLocal ? '\u672c\u5730\u5b66\u4e60\u5de5\u4f5c\u53f0' : 'ProjectB workbench'}</p>
            </div>
          </div>
          <div className="course">
            <span>{'\u8bfe\u7a0b'}</span>
            <strong>{isDemo ? 'Concurrent Systems Demo' : isLocal ? '\u64cd\u4f5c\u7cfb\u7edf' : 'Course pending'}</strong>
          </div>
          <div className="utilityStatus" aria-label={'\u8fd0\u884c\u72b6\u6001'}>
            <span className="statusPill"><LockKeyhole size={15} aria-hidden="true" />{isDemo ? 'Public demo' : isLocal ? '\u4ec5\u672c\u673a' : 'Checking profile'}</span>
            <span className="statusPill"><span className="statusDot" aria-hidden="true" />{isDemo ? 'Session-isolated synthetic data' : isLocal ? '\u672c\u5730\u6863\u6848\u6b63\u5e38' : 'Capabilities unavailable'}</span>
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
        <div className="mainInner"><RouteContent route={current} capabilities={capabilities} /></div>
      </main>
    </div>
  );
}

function RouteContent({ route, capabilities }: { route: RouteMatch; capabilities?: ApiCapabilities }) {
  if (route.id === 'import') return <ImportView importEnabled={capabilities?.profile === 'local' && capabilities.importEnabled} />;
  if (route.id === 'mapping') return <MappingView />;
  if (route.id === 'learning') return <LearningView providerEnabled={capabilities?.profile === 'local'} />;
  if (route.id === 'review') return <ReviewView />;
  if (route.id === 'settings') return <SettingsView />;
  return <NotFoundView />;
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
