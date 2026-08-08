import { createRoot } from 'react-dom/client';
import { AlertTriangle, LockKeyhole, RotateCw, Settings, ShieldCheck } from 'lucide-react';
import { routeForPath, workbenchRoutes } from './routes';
import { ImportView } from '../views/import/ImportView';
import { MappingView } from '../views/mapping/MappingView';
import '../styles/global.css';

const tasks = [
  ['区分临界区、互斥与同步', '4 道概念辨析 · 当前第 3 题', '6 分钟'],
  ['补全生产者—消费者信号量', '依据课堂讲义第 5 章生成', '8 分钟'],
  ['口述解释死锁四个必要条件', '完成后加入明日复习队列', '4 分钟'],
] as const;

const mastery = [
  ['进程与线程', '已掌握'],
  ['同步与互斥', '学习中'],
  ['死锁', '待巩固'],
  ['内存管理', '未开始'],
] as const;

export function App() {
  const path = typeof window === 'undefined' ? '/import' : window.location.pathname;
  const current = routeForPath(path);
  return (
    <div className="shell">
      <header className="shellHeader">
        <div className="utilityBar">
          <div className="brand">
            <span className="brandMark" aria-hidden="true">PB</span>
            <div><p className="brandName">ProjectB</p><p className="brandContext">本地学习工作台</p></div>
          </div>
          <div className="course"><span>课程</span><strong>操作系统</strong></div>
          <div className="utilityStatus" aria-label="运行状态">
            <span className="statusPill"><LockKeyhole size={15} aria-hidden="true" />仅本机</span>
            <span className="statusPill"><span className="statusDot" aria-hidden="true" />本地档案正常</span>
          </div>
        </div>
        <nav className="workflow" aria-label="学习流程">
          <div className="workflowInner">
            <ol className="workflowList">
              {workbenchRoutes.map((route, index) => (
                <li key={route.href}>
                  <a className="stageLink" href={route.href} aria-label={route.label} aria-current={current.href === route.href ? 'page' : undefined}>
                    <span className="stageNumber" aria-hidden="true">{index + 1}</span>
                    <span className="stageCopy"><span className="stageLabel">{route.label}</span><span className="stageDetail">{route.detail}</span></span>
                  </a>
                </li>
              ))}
            </ol>
            <a className="settingsLink" href="/settings" title="设置"><Settings size={18} aria-hidden="true" /><span>设置</span></a>
          </div>
        </nav>
      </header>
      <main>
        <div className="mainInner">
          {current.href === '/import' ? <ImportView /> : current.href === '/mapping' ? <MappingView /> : <LearningView />}
        </div>
      </main>
    </div>
  );
}

function LearningView() {
  return (
    <>
          <section className="pageIntro" aria-labelledby="page-title">
            <div><p className="eyebrow">第 3 阶段 · 今日学习</p><h1 id="page-title">练习与掌握</h1><p className="introCopy">先完成概念辨析，再处理信号量代码题。</p></div>
            <div className="progress" aria-label="今日进度 64%"><p className="progressMeta"><span>今日进度</span><strong>64%</strong></p><div className="progressTrack"><div className="progressFill" /></div></div>
          </section>
          <section className="notice" aria-label="可恢复错误">
            <div className="noticeText"><AlertTriangle size={20} aria-hidden="true" /><div><strong>有 2 页讲义尚未完成文本提取</strong><p>原文件已保留，不影响当前练习。</p></div></div>
            <button className="quietButton" type="button"><RotateCw size={15} aria-hidden="true" /> 重试</button>
          </section>
          <div className="workGrid">
            <section aria-labelledby="tasks-heading">
              <div className="sectionHeading"><div><h2 id="tasks-heading">当前任务</h2><span>3 项 · 预计 18 分钟</span></div></div>
              <ol className="taskList">{tasks.map(([title, detail, time], index) => <li className="taskRow" key={title}><span className="taskIndex">{index + 1}</span><div><p className="taskTitle">{title}</p><p className="taskDetail">{detail}</p></div><span className="taskTime">{time}</span></li>)}</ol>
            </section>
            <aside aria-labelledby="mastery-heading">
              <div className="sectionHeading"><h2 id="mastery-heading">掌握概况</h2><span>本地估算</span></div>
              <ul className="masteryList">{mastery.map(([concept, state]) => <li className="masteryRow" key={concept}><strong>{concept}</strong><span className="masteryState">{state}</span></li>)}</ul>
              <p className="privacyNote"><ShieldCheck size={17} aria-hidden="true" />进度、错题和复习计划保存在当前设备。</p>
            </aside>
          </div>
          <p className="liveRegion" role="status" aria-live="polite">ProjectB 本地档案已就绪</p>
    </>
  );
}

const rootElement = typeof document === 'undefined' ? null : document.getElementById('root');
if (rootElement) createRoot(rootElement).render(<App />);
