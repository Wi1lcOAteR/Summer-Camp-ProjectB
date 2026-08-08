import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react';
import { AlertTriangle, FileSearch, Link2, Plus, Trash2, X } from 'lucide-react';
import {
  ApiRequestError,
  createApiClient,
  type ApiClient,
  type ConceptSummary,
  type CourseSummary,
  type MaterialSummary,
  type SourceLocatorSummary,
} from '../../api/client';
import styles from './MappingView.module.css';

const defaultApi = createApiClient();

interface MappingViewProps {
  api?: Pick<ApiClient, 'listCourses' | 'listMaterials' | 'listSources' | 'listConcepts' | 'createConcept' | 'mapConcept' | 'deleteMaterial'>;
}

function locatorLabel(source: SourceLocatorSummary): string {
  if (source.kind === 'pdf_page') return `第 ${source.page} 页`;
  return source.lineStart === source.lineEnd
    ? `第 ${source.lineStart} 行`
    : `第 ${source.lineStart}-${source.lineEnd} 行`;
}

function coverageLabel(concept: ConceptSummary): string {
  if (concept.coverage?.sourceStatus === 'stale') return '来源已失效';
  if (concept.coverage?.decision === 'confirmed') return '已确认';
  if (concept.coverage?.decision === 'rejected') return '已拒绝';
  return '尚未确认';
}

export function MappingView({ api = defaultApi }: MappingViewProps) {
  const [course, setCourse] = useState<CourseSummary>();
  const [materials, setMaterials] = useState<MaterialSummary[]>([]);
  const [concepts, setConcepts] = useState<ConceptSummary[]>([]);
  const [sources, setSources] = useState<SourceLocatorSummary[]>([]);
  const [materialId, setMaterialId] = useState('');
  const [conceptId, setConceptId] = useState('');
  const [selectedLocators, setSelectedLocators] = useState<string[]>([]);
  const [conceptName, setConceptName] = useState('');
  const [evaluatorId, setEvaluatorId] = useState('os.mutex.v1');
  const [pendingDelete, setPendingDelete] = useState<MaterialSummary>();
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const cancelDeleteRef = useRef<HTMLButtonElement>(null);
  const confirmDeleteRef = useRef<HTMLButtonElement>(null);
  const materialSelectRef = useRef<HTMLSelectElement>(null);

  async function refreshWorkspace(selectedCourse = course) {
    if (!selectedCourse) return;
    const [nextMaterials, nextConcepts] = await Promise.all([
      api.listMaterials(selectedCourse.courseId),
      api.listConcepts(selectedCourse.courseId),
    ]);
    setMaterials(nextMaterials);
    setConcepts(nextConcepts);
    setMaterialId((current) => nextMaterials.some(({ materialId: id }) => id === current) ? current : nextMaterials[0]?.materialId ?? '');
    setConceptId((current) => nextConcepts.some(({ conceptId: id }) => id === current) ? current : nextConcepts[0]?.conceptId ?? '');
  }

  useEffect(() => {
    let active = true;
    void api.listCourses().then(async (items) => {
      const selected = items[0];
      if (!active || !selected) return;
      setCourse(selected);
      await refreshWorkspace(selected);
    }).catch((reason: unknown) => {
      if (active) setError(reason instanceof ApiRequestError ? reason.code : 'workspace_unavailable');
    });
    return () => { active = false; };
  }, [api]);

  useEffect(() => {
    let active = true;
    setSources([]);
    setSelectedLocators([]);
    if (!materialId) {
      return () => { active = false; };
    }
    void api.listSources(materialId).then((items) => { if (active) setSources(items); })
      .catch(() => { if (active) setError('sources_unavailable'); });
    return () => { active = false; };
  }, [api, materialId]);

  useEffect(() => {
    const selected = concepts.find(({ conceptId: id }) => id === conceptId);
    const visibleLocatorIds = new Set(sources.map(({ locatorId }) => locatorId));
    setSelectedLocators(selected?.coverage?.sourceStatus === 'current'
      ? selected.coverage.locatorIds.filter((locatorId) => visibleLocatorIds.has(locatorId))
      : []);
  }, [conceptId, concepts, sources]);

  useEffect(() => {
    if (!pendingDelete) return;
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    cancelDeleteRef.current?.focus();
    return () => {
      if (previousFocus?.isConnected) previousFocus.focus();
      else materialSelectRef.current?.focus();
    };
  }, [pendingDelete]);

  function toggleLocator(locatorId: string) {
    setSelectedLocators((current) => current.includes(locatorId)
      ? current.filter((id) => id !== locatorId)
      : [...current, locatorId]);
  }

  async function decide(decision: 'confirmed' | 'rejected') {
    if (!conceptId || selectedLocators.length === 0) {
      setError('请至少选择一个来源片段');
      return;
    }
    setBusy(true);
    setError('');
    setMessage('');
    try {
      await api.mapConcept(conceptId, selectedLocators, decision);
      await refreshWorkspace();
      setMessage(decision === 'confirmed' ? '来源映射已确认' : '来源映射已拒绝');
    } catch (reason) {
      setError(reason instanceof ApiRequestError ? reason.code : 'mapping_failed');
    } finally {
      setBusy(false);
    }
  }

  async function addConcept(event: FormEvent) {
    event.preventDefault();
    if (!course || !conceptName.trim()) return;
    setBusy(true);
    setError('');
    setMessage('');
    try {
      const created = await api.createConcept(course.courseId, conceptName.trim(), evaluatorId || null);
      await refreshWorkspace();
      setConceptId(created.conceptId);
      setConceptName('');
      setMessage('知识点已创建，尚未确认来源');
    } catch (reason) {
      setError(reason instanceof ApiRequestError ? reason.code : 'concept_create_failed');
    } finally {
      setBusy(false);
    }
  }

  async function confirmDelete() {
    if (!pendingDelete) return;
    setBusy(true);
    setError('');
    setMessage('');
    try {
      const result = await api.deleteMaterial(pendingDelete.materialId);
      await refreshWorkspace();
      setPendingDelete(undefined);
      setMessage(result.status === 'deleted' ? '材料已删除，相关来源不再具有权威性' : '删除已排队，可稍后重试');
    } catch (reason) {
      setError(reason instanceof ApiRequestError ? reason.code : 'material_delete_failed');
    } finally {
      setBusy(false);
    }
  }

  function handleDeleteKeyDown(event: KeyboardEvent<HTMLElement>) {
    if (event.key === 'Escape') {
      event.preventDefault();
      setPendingDelete(undefined);
      return;
    }
    if (event.key !== 'Tab') return;
    const controls = [cancelDeleteRef.current, confirmDeleteRef.current]
      .filter((control): control is HTMLButtonElement => Boolean(control && !control.disabled));
    if (controls.length === 0) return;
    const currentIndex = controls.indexOf(document.activeElement as HTMLButtonElement);
    const nextIndex = event.shiftKey
      ? (currentIndex <= 0 ? controls.length - 1 : currentIndex - 1)
      : (currentIndex >= controls.length - 1 ? 0 : currentIndex + 1);
    event.preventDefault();
    controls[nextIndex]?.focus();
  }

  const selectedConcept = concepts.find(({ conceptId: id }) => id === conceptId);

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="page-title">
        <div><p className="eyebrow">第 2 阶段 · 来源核对</p><h1 id="page-title">核对来源映射</h1><p className="introCopy">将具体页或文本行绑定到知识点；只有显式确认的当前来源可进入学习与计划。</p></div>
        <p className={styles.course}><span>当前课程</span><strong>{course?.name ?? '尚无课程'}</strong></p>
      </section>

      {(error || message) && <div className={error ? styles.error : styles.message} role={error ? 'alert' : 'status'}>{error && <AlertTriangle size={18} aria-hidden="true" />}<span>{error || message}</span></div>}

      <div className={styles.layout}>
        <section aria-labelledby="sources-heading">
          <div className={styles.heading}><div><h2 id="sources-heading">来源片段</h2><p>原文与定位始终可检查</p></div>
            <select ref={materialSelectRef} aria-label="选择材料" value={materialId} onChange={(event) => setMaterialId(event.target.value)}>
              {materials.length === 0 && <option value="">尚无材料</option>}
              {materials.map((material) => <option key={material.materialId} value={material.materialId}>{material.filename}</option>)}
            </select>
          </div>
          {sources.length === 0 ? <p className={styles.empty}>当前材料没有可用来源。</p> : <ul className={styles.sourceList}>{sources.map((source) => <li key={source.locatorId}>
            <label><input type="checkbox" checked={selectedLocators.includes(source.locatorId)} onChange={() => toggleLocator(source.locatorId)} aria-label={`选择 ${locatorLabel(source)}`} /><span className={styles.locator}>{locatorLabel(source)}</span><span className={styles.sourceText}>{source.text}</span></label>
          </li>)}</ul>}
          {materials.map((material) => material.materialId === materialId && <button key={material.materialId} className={styles.deleteButton} type="button" aria-label={`删除 ${material.filename}`} title={`删除 ${material.filename}`} onClick={() => setPendingDelete(material)}><Trash2 size={16} aria-hidden="true" />删除材料</button>)}
        </section>

        <section aria-labelledby="concepts-heading">
          <div className={styles.heading}><div><h2 id="concepts-heading">知识点</h2><p>未确认映射不具有权威性</p></div></div>
          <form className={styles.conceptForm} onSubmit={(event) => void addConcept(event)}>
            <label><span>名称</span><input value={conceptName} onChange={(event) => setConceptName(event.target.value)} maxLength={120} /></label>
            <label><span>检查方式</span><select value={evaluatorId} onChange={(event) => setEvaluatorId(event.target.value)}><option value="os.mutex.v1">互斥</option><option value="os.race.v1">竞态</option><option value="os.deadlock.v1">死锁</option><option value="">仅解释</option></select></label>
            <button type="submit" disabled={busy || !conceptName.trim()} title="新增知识点"><Plus size={16} aria-hidden="true" />新增</button>
          </form>
          {concepts.length === 0 ? <p className={styles.empty}>创建知识点后再选择来源。</p> : <ul className={styles.conceptList}>{concepts.map((concept) => <li key={concept.conceptId} className={concept.conceptId === conceptId ? styles.activeConcept : undefined}>
            <button type="button" onClick={() => setConceptId(concept.conceptId)}><span><strong>{concept.name}</strong><small>{concept.state === 'explanation_only' ? '仅解释' : concept.evaluatorId}</small></span><em className={concept.coverage?.sourceStatus === 'stale' ? styles.stale : undefined}>{coverageLabel(concept)}</em></button>
          </li>)}</ul>}
          <label className={styles.conceptSelect}><span>选择知识点</span><select aria-label="选择知识点" value={conceptId} onChange={(event) => setConceptId(event.target.value)}><option value="">请选择</option>{concepts.map((concept) => <option key={concept.conceptId} value={concept.conceptId}>{concept.name}</option>)}</select></label>
          <div className={styles.selectionStatus}><FileSearch size={18} aria-hidden="true" /><div><strong>{selectedConcept ? coverageLabel(selectedConcept) : '尚未选择'}</strong><p>{selectedLocators.length} 个来源片段已选择</p></div></div>
          <div className={styles.actions}><button type="button" className={styles.secondary} disabled={busy || !conceptId || selectedLocators.length === 0} onClick={() => void decide('rejected')}><X size={16} aria-hidden="true" />拒绝映射</button><button type="button" className={styles.primary} disabled={busy || !conceptId || selectedLocators.length === 0} onClick={() => void decide('confirmed')}><Link2 size={16} aria-hidden="true" />确认来源</button></div>
        </section>
      </div>

      {pendingDelete && <div className={styles.scrim}><section className={styles.dialog} role="dialog" aria-modal="true" aria-labelledby="delete-title" onKeyDown={handleDeleteKeyDown}><h2 id="delete-title">确认删除材料</h2><p>将删除“{pendingDelete.filename}”在当前课程中的引用，相关来源会立即失效。</p><div className={styles.actions}><button ref={cancelDeleteRef} type="button" className={styles.secondary} onClick={() => setPendingDelete(undefined)}>取消</button><button ref={confirmDeleteRef} type="button" className={styles.danger} disabled={busy} onClick={() => void confirmDelete()}>确认删除</button></div></section></div>}
    </div>
  );
}
