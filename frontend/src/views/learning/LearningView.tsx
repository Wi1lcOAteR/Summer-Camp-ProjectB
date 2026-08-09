import { useEffect, useMemo, useState } from 'react';
import { BadgeCheck, BookOpenText, CircleAlert, FileCheck2, Send, ShieldCheck, Sparkles } from 'lucide-react';
import {
  ApiRequestError,
  createApiClient,
  type ApiClient,
  type ConceptSummary,
  type CourseSummary,
  type MaterialSummary,
  type SourceLocatorSummary,
} from '../../api/client';
import styles from './LearningView.module.css';

interface LearningViewProps {
  api?: Pick<ApiClient, 'listCourses' | 'listMaterials' | 'listSources' | 'listConcepts'>;
  providerEnabled?: boolean;
}

type LearningConcept = ConceptSummary & {
  source?: LearningSource;
  material?: MaterialSummary;
};

type LearningSource = SourceLocatorSummary & { materialId: string };

const rubric = [
  { code: 'mutual_exclusion', detail: '检查临界区是否存在同时进入的线程。' },
  { code: 'witness_matches', detail: '检查选择的结论是否与给出的执行轨迹一致。' },
] as const;

const maxTokens = 320;
const maxCost = 'USD 0.01';
const defaultApi = createApiClient();

function sourceIsCurrent(concept: LearningConcept): concept is LearningConcept & { source: LearningSource } {
  return concept.coverage?.decision === 'confirmed'
    && concept.coverage.sourceStatus === 'current'
    && Boolean(concept.source);
}

function errorCode(reason: unknown): string {
  return reason instanceof ApiRequestError ? reason.code : 'learning_unavailable';
}

export function LearningView({ api = defaultApi, providerEnabled = true }: LearningViewProps) {
  const [course, setCourse] = useState<CourseSummary>();
  const [concepts, setConcepts] = useState<LearningConcept[]>([]);
  const [conceptId, setConceptId] = useState('');
  const [holds, setHolds] = useState('true');
  const [answer, setAnswer] = useState('');
  const [checked, setChecked] = useState(false);
  const [providerPreview, setProviderPreview] = useState(false);
  const [providerConfirmed, setProviderConfirmed] = useState(false);
  const [providerStatus, setProviderStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const selectedCourse = (await api.listCourses())[0];
        if (!selectedCourse) throw new ApiRequestError('course_unavailable');
        const [materials, conceptRows] = await Promise.all([
          api.listMaterials(selectedCourse.courseId),
          api.listConcepts(selectedCourse.courseId),
        ]);
        const sourcesByMaterial = await Promise.all(materials.map(async (material) => (
          [material, await api.listSources(material.materialId)] as const
        )));
        const sources = sourcesByMaterial.flatMap(([material, items]) => items.map((source) => ({ ...source, materialId: material.materialId })));
        const nextConcepts = conceptRows.map((concept) => {
          const source = concept.coverage?.locatorIds
            .map((locatorId) => sources.find((item) => item.locatorId === locatorId))
            .find((item): item is LearningSource => Boolean(item));
          const material = materials.find((item) => item.materialId === source?.materialId);
          return { ...concept, source, material };
        });
        if (!active) return;
        setCourse(selectedCourse);
        setConcepts(nextConcepts);
        setConceptId(nextConcepts[0]?.conceptId ?? '');
      } catch (reason) {
        if (active) setError(errorCode(reason));
      } finally {
        if (active) setLoading(false);
      }
    }
    void load();
    return () => { active = false; };
  }, [api]);

  const concept = useMemo(
    () => concepts.find((item) => item.conceptId === conceptId) ?? concepts[0],
    [conceptId, concepts],
  );
  const sourceBound = concept ? sourceIsCurrent(concept) : false;
  const explanationOnly = concept?.state === 'explanation_only';
  const canEvaluate = sourceBound && !explanationOnly && Boolean(concept?.evaluatorId);
  const deterministicPass = holds === 'true';

  function changeConcept(nextId: string) {
    setConceptId(nextId);
    setChecked(false);
    setAnswer('');
    setProviderPreview(false);
    setProviderConfirmed(false);
    setProviderStatus('');
  }

  function previewProvider() {
    if (!sourceBound) {
      setError('source_unavailable');
      return;
    }
    setProviderPreview(true);
    setProviderConfirmed(false);
    setProviderStatus('');
  }

  function confirmProvider() {
    setProviderStatus('已确认预览；当前未发送任何提供方请求。');
  }

  function submitCheck() {
    if (!canEvaluate) {
      setError('source_unavailable');
      return;
    }
    setChecked(true);
    setError('');
  }

  if (loading) return <p role="status">正在读取学习数据…</p>;
  if (error && !concept) return <p role="alert">学习数据不可用：{error}</p>;
  if (!concept) return <p role="status">暂无可学习知识点。</p>;

  const source = concept.source;
  const locatorLabel = source?.kind === 'pdf_page'
    ? `第 ${source.page} 页`
    : source ? `第 ${source.lineStart}-${source.lineEnd} 行` : '来源不可用';
  const evidenceId = source ? `evidence-${concept.conceptId}-${source.locatorId}` : '';

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="page-title">
        <div>
          <p className="eyebrow">第 3 阶段 · 来源绑定学习</p>
          <h1 id="page-title">学习与练习</h1>
          <p className="introCopy">解释、练习和每项检查都保持可追溯；模型文字不构成评分或掌握度。</p>
        </div>
        <p className={styles.mode}><span>当前课程</span><strong>{course?.name ?? '本地课程'}</strong></p>
      </section>

      {error && <p className={styles.error} role="alert">学习数据不可用：{error}</p>}

      <div className={styles.layout}>
        <div className={styles.primaryColumn}>
          <section className={styles.section} aria-labelledby="concept-heading">
            <div className={styles.heading}>
              <div><h2 id="concept-heading">知识点与来源</h2><p>只显示已确认且当前有效的来源片段。</p></div>
              <label className={styles.selectLabel}><span>选择知识点</span><select aria-label="选择知识点" value={concept.conceptId} onChange={(event) => changeConcept(event.target.value)}>
                {concepts.map((item) => <option key={item.conceptId} value={item.conceptId}>{item.name}</option>)}
              </select></label>
            </div>
            {sourceBound && source ? <div className={styles.source}>
              <BookOpenText size={21} aria-hidden="true" />
              <div><strong>{source.text}</strong><p><span className={styles.confirmed}>来源已确认</span>{concept.material?.filename ?? '当前材料'}，{locatorLabel}</p><dl className={styles.sourceIdentity}><div><dt>版本</dt><dd>{source.materialVersionId}</dd></div><div><dt>内容 hash</dt><dd>{source.contentHash}</dd></div><div><dt>coverage</dt><dd>{concept.coverage?.version}</dd></div></dl></div>
            </div> : <div className={styles.explanationOnly} role="status"><CircleAlert size={20} aria-hidden="true" /><div><strong>{explanationOnly ? '仅解释' : '来源不可用'}</strong><p>{explanationOnly ? '该知识点没有确定性 rubric，不能提交练习、生成证据或更新掌握度。' : '来源未确认、已过期或缺少不可变身份，学习与 P 预览均已禁用。'}</p></div></div>}
          </section>

          <section className={styles.section} aria-labelledby="explanation-heading">
            <div className={styles.heading}><div><h2 id="explanation-heading">来源解释</h2><p>本地示例解释，依据上方片段而非模型权威。</p></div><span className={styles.localLabel}>本地解释</span></div>
            <p className={styles.explanation}>{concept.name} 的判断必须回到已确认来源。当前示例通过一个可复现的轨迹练习呈现规则与证据，不自动推断掌握度。</p>
          </section>

          <section className={styles.section} aria-labelledby="practice-heading">
            <div className={styles.heading}><div><h2 id="practice-heading">确定性练习</h2><p>练习由版本化规则检查；原始答案只保留在本地输入框。</p></div><span className={styles.ruleLabel}>{concept.evaluatorId ?? '仅解释'}</span></div>
            {explanationOnly ? <div className={styles.explanationOnly} role="status"><CircleAlert size={20} aria-hidden="true" /><div><strong>仅解释</strong><p>该知识点没有确定性 rubric，不能提交练习、生成证据或更新掌握度。</p></div></div> : <fieldset className={styles.practice} disabled={!canEvaluate}>
              <legend>执行轨迹：线程 A 已进入临界区，线程 B 尝试进入。</legend>
              <label><span>互斥是否成立</span><select aria-label="互斥是否成立" value={holds} onChange={(event) => setHolds(event.target.value)}><option value="true">成立</option><option value="false">不成立</option></select></label>
              <label><span>我的答案</span><textarea value={answer} onChange={(event) => setAnswer(event.target.value)} maxLength={800} placeholder="仅在本地用于你的练习记录" /></label>
              <button type="button" className={styles.primaryButton} onClick={submitCheck}><BadgeCheck size={17} aria-hidden="true" />提交确定性检查</button>
            </fieldset>}
          </section>

          {providerEnabled && <section className={styles.section} aria-labelledby="provider-heading">
            <div className={styles.heading}><div><h2 id="provider-heading">P 提供方辅助</h2><p>可选的外部文字辅助，与确定性评分和掌握度隔离。</p></div><span className={styles.providerLabel}>P · 外部提供方</span></div>
            <div className={styles.providerIntro}><Sparkles size={19} aria-hidden="true" /><p>可以基于已确认的来源片段请求解释措辞或练习候选。未确认时不会发送请求。</p><button type="button" className={styles.secondaryButton} onClick={previewProvider} disabled={!sourceBound}>查看 P 提供方预览</button></div>
            {providerPreview && source && <section className={styles.preview} aria-label="P 提供方预览">
              <h3>发送前预览</h3>
              <dl><div><dt>来源 locator</dt><dd>{source.locatorId}</dd></div><div><dt>材料版本</dt><dd>{source.materialVersionId}</dd></div><div><dt>内容 hash</dt><dd>{source.contentHash}</dd></div><div><dt>抽取片段</dt><dd>{source.text}</dd></div><div><dt>端口</dt><dd>generate_explanation</dd></div><div><dt>模型 profile</dt><dd>P / OpenAI adapter</dd></div><div><dt>上限</dt><dd>最多 {maxTokens} tokens，最高 {maxCost}</dd></div><div><dt>政策</dt><dd>仅发送已确认片段；store=false；无文件、工具或整份材料上传。</dd></div><div><dt>排除</dt><dd>不包含原始答案、评分结果、掌握度或本地文件。</dd></div></dl>
              <label className={styles.consent}><input type="checkbox" checked={providerConfirmed} onChange={(event) => setProviderConfirmed(event.target.checked)} />我确认以上预览内容可以发送</label>
              <button type="button" className={styles.primaryButton} disabled={!providerConfirmed} onClick={confirmProvider}><Send size={17} aria-hidden="true" />确认预览</button>
              {providerStatus && <p className={styles.providerStatus} role="status">{providerStatus}</p>}
            </section>}
          </section>}
        </div>

        <aside className={styles.evidenceColumn} aria-label="确定性检查与证据">
          <section className={styles.section} aria-labelledby="rubric-heading">
            <div className={styles.heading}><div><h2 id="rubric-heading">确定性规则</h2><p>规则版本 {concept.evaluatorId ?? '无'}。</p></div><ShieldCheck size={20} aria-hidden="true" /></div>
            {explanationOnly ? <p className={styles.empty}>该知识点没有确定性 rubric。</p> : <ul className={styles.rubricList}>{rubric.map((item) => <li key={item.code}><strong>{item.code}</strong><span>{item.detail}</span><em className={checked && deterministicPass ? styles.passed : undefined}>{checked ? (deterministicPass ? '通过' : '未通过') : '待检查'}</em></li>)}</ul>}
          </section>
          <section className={styles.section} aria-labelledby="evidence-heading">
            <div className={styles.heading}><div><h2 id="evidence-heading">证据</h2><p>确定性检查的附加记录。</p></div><FileCheck2 size={20} aria-hidden="true" /></div>
            {explanationOnly ? <p className={styles.empty}>该知识点不产生确定性证据。</p> : checked && source ? <dl className={styles.evidence}><div><dt>证据 ID</dt><dd>{evidenceId}</dd></div><div><dt>来源</dt><dd>{source.locatorId}</dd></div><div><dt>状态</dt><dd>{deterministicPass ? '已通过' : '需复核'}</dd></div><div><dt>模型内容</dt><dd>不参与评分或掌握度</dd></div></dl> : <p className={styles.empty}>提交检查后才会生成证据。</p>}
          </section>
          {checked && !explanationOnly && <p className={styles.feedback} role="status">{deterministicPass ? '反馈：轨迹符合互斥规则。请继续核对来源和后续变体。' : '反馈：轨迹出现重叠进入。请回到来源片段核对临界区边界。'}</p>}
        </aside>
      </div>
    </div>
  );
}
