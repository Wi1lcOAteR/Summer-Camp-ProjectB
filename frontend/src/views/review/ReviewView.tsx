import { Check, RotateCcw, SkipForward } from 'lucide-react';
import { useState } from 'react';
import styles from './ReviewView.module.css';

type ReviewMode = 'continuous' | 'finals';

type MasteryState = 'unknown' | 'demonstrated_now' | 'retained';

interface ReviewItem {
  id: string;
  label: string;
  state: '已完成' | '待复习';
  mastery: MasteryState;
  source: string;
}

const items: ReviewItem[] = [
  { id: 'mutex', label: '互斥', state: '已完成', mastery: 'demonstrated_now', source: '讲义第 12-14 行' },
  { id: 'race', label: '竞态条件', state: '待复习', mastery: 'unknown', source: '讲义第 27-31 行' },
  { id: 'deadlock', label: '死锁', state: '待复习', mastery: 'unknown', source: '讲义第 42-47 行' },
];

const sourceHash = 'a'.repeat(64);
const masteryLabels: Record<MasteryState, string> = {
  unknown: '起步',
  demonstrated_now: '熟练',
  retained: '保留',
};

const baseIntervals = [1, 3, 7, 14, 30] as const;
const finalsIntervals: Record<MasteryState, readonly number[]> = {
  unknown: [1, 2, 4, 7, 15],
  demonstrated_now: [1, 3, 6, 11, 23],
  retained: baseIntervals,
};

function addDays(localDate: string, days: number): string {
  const value = new Date(`${localDate}T00:00:00Z`);
  value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}

export function ReviewView() {
  const [mode, setMode] = useState<ReviewMode>('continuous');
  const [dailyBudget, setDailyBudget] = useState(30);
  const [compressed, setCompressed] = useState(true);
  const [cutoff, setCutoff] = useState('今天 21:00');
  const [examDate, setExamDate] = useState(() => addDays(new Date().toISOString().slice(0, 10), 30));
  const [recovered, setRecovered] = useState(false);
  const [message, setMessage] = useState('');

  const today = new Date().toISOString().slice(0, 10);
  const pastExam = mode === 'finals' && examDate < today;
  const budgetValid = dailyBudget >= 10 && dailyBudget <= 120 && dailyBudget % 5 === 0;
  const tasksByDate = new Map<string, ReviewItem[]>();
  if (!pastExam && budgetValid) {
    for (const item of items) {
      const intervals = mode === 'continuous' ? baseIntervals : finalsIntervals[item.mastery];
      for (const interval of intervals) {
        const due = addDays(today, interval);
        if (mode === 'finals' && due > examDate) continue;
        tasksByDate.set(due, [...(tasksByDate.get(due) ?? []), item]);
      }
    }
  }
  const capacity = Math.floor(dailyBudget / 10);
  const scheduledCount = [...tasksByDate.values()].reduce(
    (total, dueItems) => total + Math.min(capacity, dueItems.length),
    0,
  );

  function selectMode(next: ReviewMode) {
    setMode(next);
    setMessage(next === 'finals' ? '最终复习已选择' : '连续复习已选择');
  }

  function recover() {
    setRecovered(true);
    setMessage('已恢复 2 个未完成项；已完成任务保持不变');
  }

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="page-title">
        <div>
          <p className="eyebrow">第 4 阶段 · 复习编排</p>
          <h1 id="page-title">复习计划</h1>
          <p className="introCopy">按当前来源和掌握状态安排下一轮复习；计划变更不会重写已完成任务。</p>
        </div>
        <p className={styles.status}><span>计划状态</span><strong>本地草案 · 可恢复</strong></p>
      </section>

      {message && <p className={styles.message} role="status">{message}</p>}

      <div className={styles.layout}>
        <div className={styles.primary}>
          <section className={styles.section} aria-labelledby="budget-heading">
            <div className={styles.heading}><div><h2 id="budget-heading">今日预算</h2><p>只使用本地确定性计划</p></div><strong className={styles.budget}>{dailyBudget} 分钟</strong></div>
            <div className={styles.metrics}>
              <div><span>可安排任务</span><strong>{scheduledCount}</strong></div>
              <div><span>3 个来源</span><strong>3</strong></div>
              <div><span>计划总量</span><strong>{scheduledCount * 10} 分钟</strong></div>
            </div>
          </section>

          <section className={styles.section} aria-labelledby="controls-heading">
            <div className={styles.heading}><div><h2 id="controls-heading">计划控制</h2><p>调整节奏和截止时间</p></div></div>
            <fieldset className={styles.controls}>
              <legend>复习模式</legend>
              <div className={styles.segmented} role="radiogroup" aria-label="复习模式">
                <label><input type="radio" name="mode" value="continuous" checked={mode === 'continuous'} onChange={() => selectMode('continuous')} />连续复习</label>
                <label><input type="radio" name="mode" value="finals" checked={mode === 'finals'} onChange={() => selectMode('finals')} />最终复习</label>
              </div>
              <label className={styles.cutoff}>每日预算（分钟）<input aria-label="每日预算（分钟）" type="number" min="10" max="120" step="5" value={dailyBudget} onChange={(event) => setDailyBudget(Number(event.target.value))} /></label>
              <label className={styles.check}><input type="checkbox" checked={compressed} onChange={(event) => setCompressed(event.target.checked)} /> <span>压缩重复项</span></label>
              <label className={styles.cutoff}>截止时间<input aria-label="截止时间" value={cutoff} onChange={(event) => setCutoff(event.target.value)} /></label>
              {mode === 'finals' && <label className={styles.cutoff}>考试日期<input aria-label="考试日期" type="date" value={examDate} onChange={(event) => setExamDate(event.target.value)} /></label>}
              {!budgetValid && <p role="alert">预算必须为 10 到 120 分钟，且按 5 分钟递增。</p>}
              {pastExam && <p role="alert">考试日期已过去，计划已归档。</p>}
            </fieldset>
          </section>

          <section className={styles.section} aria-labelledby="diff-heading" aria-label="计划修订差异">
            <div className={styles.heading}><div><h2 id="diff-heading">计划修订差异</h2><p>本次调整相对上一版计划</p></div></div>
            <div className={styles.diff}><p><span className={styles.removed}>{compressed ? '− 删除同日重复练习' : '− 未删除重复练习'}</span><span className={styles.added}>{pastExam ? '+ 截止日期前无可安排任务' : `+ 当前 revision 安排 ${scheduledCount} 个任务`}</span></p><p className={styles.diffNote}>{pastExam ? '考试日期已过，revision 进入归档状态。' : compressed ? '已按 evidence weakness 压缩同日重复项。' : '未压缩重复项，保留完整练习轨迹。'}</p></div>
          </section>

          <section className={styles.section} aria-labelledby="completion-heading">
            <div className={styles.heading}><div><h2 id="completion-heading">完成与恢复</h2><p>完成记录只读；未完成项可以恢复</p></div></div>
            <ul className={styles.taskList}>
              {items.map((item) => <li key={item.id}><span className={item.state === '已完成' ? styles.doneIcon : styles.pendingIcon}>{item.state === '已完成' ? <Check size={15} aria-hidden="true" /> : '·'}</span><span className={styles.taskCopy}><strong>{item.state === '待复习' && recovered ? `恢复中 · ${item.label}` : `${item.state} · ${item.label}`}</strong><small>{item.source}</small></span><em data-mastery={item.mastery}>{masteryLabels[item.mastery]}</em></li>)}
            </ul>
            <div className={styles.actions}><button type="button" className={styles.primaryButton}><Check size={16} aria-hidden="true" />开始复习</button><button type="button" className={styles.secondaryButton} onClick={recover}><RotateCcw size={16} aria-hidden="true" />恢复未完成项</button><button type="button" className={styles.iconButton} title="跳过当前计划" aria-label="跳过当前计划"><SkipForward size={16} aria-hidden="true" /></button></div>
          </section>
        </div>

        <aside className={styles.aside}>
          <section className={styles.section} aria-labelledby="sources-heading"><div className={styles.heading}><div><h2 id="sources-heading">来源摘要</h2><p>已确认的材料身份</p></div></div><div className={styles.sourceCard}><strong>操作系统讲义.txt</strong><span>3 个来源 · material-version-1</span><code>sha256: {sourceHash}</code><p>当前版本 · 内容 hash 已确认</p></div></section>
          <section className={styles.section} aria-labelledby="mastery-heading"><div className={styles.heading}><div><h2 id="mastery-heading">掌握度</h2><p>按最近一次确定性检查</p></div></div><div className={styles.mastery}><div><span>demonstrated_now · 熟练</span><strong>1</strong></div><div><span>retained · 保留</span><strong>0</strong></div><div><span>unknown · 起步</span><strong>2</strong></div></div></section>
          <section className={styles.section} aria-labelledby="status-heading"><div className={styles.heading}><div><h2 id="status-heading">当前设置</h2></div></div><dl className={styles.settings}><div><dt>模式</dt><dd>{mode === 'finals' ? '最终复习' : '连续复习'}</dd></div><div><dt>预算</dt><dd>{dailyBudget} 分钟</dd></div><div><dt>压缩</dt><dd>{compressed ? '开启' : '关闭'}</dd></div><div><dt>截止</dt><dd>{cutoff || '未设置'}</dd></div>{mode === 'finals' && <div><dt>考试日期</dt><dd>{examDate}</dd></div>}</dl></section>
        </aside>
      </div>
    </div>
  );
}
