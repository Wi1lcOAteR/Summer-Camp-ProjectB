import { Check, RefreshCw, RotateCcw, SkipForward } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import {
  ApiRequestError,
  createApiClient,
  type ApiClient,
  type ConceptSummary,
  type CourseSummary,
  type ReviewRevisionSummary,
  type ReviewTaskSummary,
} from '../../api/client';
import styles from './ReviewView.module.css';

type ReviewMode = 'continuous' | 'finals';

interface ReviewViewProps {
  api?: Pick<ApiClient, 'listCourses' | 'listConcepts' | 'generateReviewRevision' | 'completeReviewTask' | 'skipReviewTask' | 'recoverReviewTask'>;
  now?: () => Date;
}

const defaultApi = createApiClient();
const systemNow = () => new Date();

function errorCode(reason: unknown): string {
  return reason instanceof ApiRequestError ? reason.code : 'review_unavailable';
}

function statusLabel(status: ReviewTaskSummary['status']): string {
  if (status === 'completed') return '已完成';
  if (status === 'skipped') return '已跳过';
  return '待复习';
}

export function ReviewView({ api = defaultApi, now = systemNow }: ReviewViewProps) {
  const [course, setCourse] = useState<CourseSummary>();
  const [concepts, setConcepts] = useState<ConceptSummary[]>([]);
  const [revision, setRevision] = useState<ReviewRevisionSummary>();
  const [mode, setMode] = useState<ReviewMode>('continuous');
  const [dailyBudget, setDailyBudget] = useState(30);
  const [examDate, setExamDate] = useState(() => {
    const value = new Date(); value.setDate(value.getDate() + 30); return value.toISOString().slice(0, 10);
  });
  const [activeTaskId, setActiveTaskId] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  async function generate(selectedCourse: CourseSummary, nextMode = mode, nextBudget = dailyBudget, nextExam = examDate) {
    setSaving(true); setError('');
    try {
      const next = await api.generateReviewRevision({
        courseId: selectedCourse.courseId,
        mode: nextMode,
        timezone: selectedCourse.timezone,
        dailyBudgetMinutes: nextBudget,
        examDate: nextMode === 'finals' ? nextExam : undefined,
        generatedAt: now().toISOString(),
      });
      setRevision(next);
      setActiveTaskId((current) => next.tasks.some((task) => task.taskId === current && task.status === 'pending') ? current : '');
      setMessage('复习计划已按当前学习证据生成');
    } catch (reason) {
      setError(errorCode(reason));
    } finally {
      setSaving(false);
    }
  }

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const selectedCourse = (await api.listCourses())[0];
        if (!selectedCourse) throw new ApiRequestError('course_unavailable');
        const conceptRows = await api.listConcepts(selectedCourse.courseId);
        if (!active) return;
        setCourse(selectedCourse); setConcepts(conceptRows);
        const next = await api.generateReviewRevision({
          courseId: selectedCourse.courseId,
          mode: 'continuous',
          timezone: selectedCourse.timezone,
          dailyBudgetMinutes: 30,
          generatedAt: now().toISOString(),
        });
        if (active) setRevision(next);
      } catch (reason) {
        if (active) setError(errorCode(reason));
      } finally {
        if (active) setLoading(false);
      }
    }
    void load();
    return () => { active = false; };
  }, [api, now]);

  const conceptNames = useMemo(() => new Map(concepts.map((concept) => [concept.conceptId, concept.name])), [concepts]);
  const tasks = revision?.tasks ?? [];
  const pending = tasks.filter((task) => task.status === 'pending');
  const skipped = tasks.filter((task) => task.status === 'skipped');
  const completed = tasks.filter((task) => task.status === 'completed');
  const activeTask = tasks.find((task) => task.taskId === activeTaskId);
  const sourceCount = new Set(tasks.flatMap((task) => task.sourceRefs)).size;
  const evidenceCount = new Set(tasks.flatMap((task) => task.evidenceRefs)).size;

  function replaceTask(next: ReviewTaskSummary) {
    setRevision((current) => current ? { ...current, tasks: current.tasks.map((task) => task.taskId === next.taskId ? next : task) } : current);
  }

  function start() {
    const task = pending[0];
    if (!task) { setMessage('当前没有待复习任务'); return; }
    setActiveTaskId(task.taskId);
    setMessage(`正在复习：${conceptNames.get(task.conceptId) ?? task.conceptId}`);
  }

  async function complete() {
    if (!activeTask) return;
    setSaving(true); setError('');
    try {
      const next = await api.completeReviewTask(activeTask.taskId, now().toISOString());
      replaceTask(next); setActiveTaskId(''); setMessage('当前复习任务已完成并保存');
    } catch (reason) { setError(errorCode(reason)); } finally { setSaving(false); }
  }

  async function skip() {
    const task = activeTask ?? pending[0];
    if (!task) { setMessage('当前没有可跳过任务'); return; }
    setSaving(true); setError('');
    try {
      const next = await api.skipReviewTask(task.taskId);
      replaceTask(next); setActiveTaskId(''); setMessage('任务已跳过，可稍后恢复');
    } catch (reason) { setError(errorCode(reason)); } finally { setSaving(false); }
  }

  async function recover() {
    const task = skipped[0];
    if (!task) { setMessage('当前没有已跳过任务'); return; }
    setSaving(true); setError('');
    try {
      const next = await api.recoverReviewTask(task.taskId);
      replaceTask(next); setMessage('已跳过任务已恢复');
    } catch (reason) { setError(errorCode(reason)); } finally { setSaving(false); }
  }

  if (loading) return <p role="status">正在生成复习计划…</p>;
  if (!course || !revision) return <p role="alert">复习计划不可用：{error || 'review_unavailable'}</p>;

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="page-title">
        <div><p className="eyebrow">第 4 阶段 · 复习编排</p><h1 id="page-title">复习计划</h1><p className="introCopy">按已确认来源和学习证据生成任务；完成、跳过和恢复会写入本地数据库。</p></div>
        <p className={styles.status}><span>当前课程</span><strong>{course.name}</strong></p>
      </section>
      {message && <p className={styles.message} role="status">{message}</p>}
      {error && <p role="alert">操作失败：{error}</p>}

      <div className={styles.layout}>
        <div className={styles.primary}>
          <section className={styles.section} aria-labelledby="budget-heading">
            <div className={styles.heading}><div><h2 id="budget-heading">真实计划概览</h2><p>revision {revision.revisionId.slice(0, 18)}…</p></div><strong className={styles.budget}>{tasks.reduce((sum, task) => sum + task.durationMinutes, 0)} 分钟</strong></div>
            <div className={styles.metrics}><div><span>待复习</span><strong>{pending.length}</strong></div><div><span>已完成</span><strong>{completed.length}</strong></div><div><span>已跳过</span><strong>{skipped.length}</strong></div></div>
          </section>

          <section className={styles.section} aria-labelledby="controls-heading">
            <div className={styles.heading}><div><h2 id="controls-heading">计划控制</h2><p>修改后点击更新计划</p></div></div>
            <fieldset className={styles.controls}><legend>复习模式</legend>
              <div className={styles.segmented} role="radiogroup" aria-label="复习模式"><label><input type="radio" name="mode" value="continuous" checked={mode === 'continuous'} onChange={() => setMode('continuous')} />连续复习</label><label><input type="radio" name="mode" value="finals" checked={mode === 'finals'} onChange={() => setMode('finals')} />最终复习</label></div>
              <label className={styles.cutoff}>每日预算（分钟）<input aria-label="每日预算（分钟）" type="number" min="10" max="120" step="5" value={dailyBudget} onChange={(event) => setDailyBudget(Number(event.target.value))} /></label>
              {mode === 'finals' && <label className={styles.cutoff}>考试日期<input aria-label="考试日期" type="date" value={examDate} onChange={(event) => setExamDate(event.target.value)} /></label>}
              <button type="button" className={styles.secondaryButton} disabled={saving || dailyBudget < 10 || dailyBudget > 120 || dailyBudget % 5 !== 0} onClick={() => void generate(course)}><RefreshCw size={16} aria-hidden="true" />更新计划</button>
            </fieldset>
          </section>

          <section className={styles.section} aria-labelledby="diff-heading" aria-label="计划修订差异">
            <div className={styles.heading}><div><h2 id="diff-heading">计划修订差异</h2><p>由后端 revision 计算</p></div></div>
            <div className={styles.diff}><p><span className={styles.added}>+ 新增 {revision.diff.added.length}</span><span className={styles.removed}>− 移除 {revision.diff.removed.length}</span><span>变更 {revision.diff.changed.length} · 保留 {revision.diff.retained.length}</span></p></div>
          </section>

          <section className={styles.section} aria-labelledby="completion-heading">
            <div className={styles.heading}><div><h2 id="completion-heading">任务</h2><p>状态变更会持久化</p></div></div>
            {tasks.length === 0 ? <p>当前没有可安排任务，请先在学习页完成来源确认和练习。</p> : <ul className={styles.taskList}>{tasks.map((task) => {
              const label = conceptNames.get(task.conceptId) ?? task.conceptId;
              return <li key={task.taskId}><span className={task.status === 'completed' ? styles.doneIcon : styles.pendingIcon}>{task.status === 'completed' ? <Check size={15} aria-hidden="true" /> : '·'}</span><span className={styles.taskCopy}><strong>{statusLabel(task.status)} · {label}</strong><small>{task.dueLocalDate} · {task.durationMinutes} 分钟</small></span><em>{task.sourceRefs.length} 个来源</em></li>;
            })}</ul>}
            <div className={styles.actions}>
              {!activeTask && <button type="button" className={styles.primaryButton} disabled={saving || pending.length === 0} onClick={start}><Check size={16} aria-hidden="true" />开始复习</button>}
              {activeTask && <button type="button" className={styles.primaryButton} disabled={saving} onClick={() => void complete()}><Check size={16} aria-hidden="true" />完成当前任务</button>}
              <button type="button" className={styles.secondaryButton} disabled={saving || skipped.length === 0} onClick={() => void recover()}><RotateCcw size={16} aria-hidden="true" />恢复已跳过任务</button>
              <button type="button" className={styles.iconButton} disabled={saving || pending.length === 0} title="跳过当前任务" aria-label="跳过当前任务" onClick={() => void skip()}><SkipForward size={16} aria-hidden="true" /></button>
            </div>
          </section>
        </div>

        <aside className={styles.aside}>
          <section className={styles.section} aria-labelledby="sources-heading"><div className={styles.heading}><div><h2 id="sources-heading">来源与证据</h2><p>来自当前 revision</p></div></div><div className={styles.sourceCard}><strong>{sourceCount} 个已确认来源</strong><span>{evidenceCount} 条学习 evidence</span><code>input hash: {revision.inputHash}</code><p>不再使用演示文件名或占位 hash。</p></div></section>
          <section className={styles.section} aria-labelledby="status-heading"><div className={styles.heading}><div><h2 id="status-heading">当前设置</h2></div></div><dl className={styles.settings}><div><dt>模式</dt><dd>{mode === 'finals' ? '最终复习' : '连续复习'}</dd></div><div><dt>预算</dt><dd>{dailyBudget} 分钟</dd></div><div><dt>任务</dt><dd>{tasks.length}</dd></div>{mode === 'finals' && <div><dt>考试日期</dt><dd>{examDate}</dd></div>}</dl></section>
        </aside>
      </div>
    </div>
  );
}
