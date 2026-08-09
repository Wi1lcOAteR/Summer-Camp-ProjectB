import { useEffect, useRef, useState } from 'react';
import { AlertTriangle, CheckCircle2, FileText, Upload, X } from 'lucide-react';
import {
  ApiRequestError,
  createApiClient,
  type ApiClient,
  type CourseSummary,
  type MaterialImportResult,
  type MaterialSummary,
} from '../../api/client';
import styles from './ImportView.module.css';

const defaultApi = createApiClient();
const MAX_FILES = 5;
const MAX_FILE_BYTES = 20 * 1024 * 1024;
const MAX_BATCH_BYTES = 50 * 1024 * 1024;
const acceptedExtensions = new Set(['pdf', 'txt', 'md']);

interface ImportViewProps {
  api?: Pick<ApiClient, 'listCourses' | 'createCourse' | 'listMaterials' | 'importMaterials'>;
  importEnabled?: boolean;
}

interface DisplayResult extends MaterialImportResult {
  filename: string;
}

function errorMessage(code: string): string {
  const messages: Record<string, string> = {
    batch_file_limit: '每次最多选择 5 个文件',
    batch_byte_limit: '本批文件总大小超过 50 MiB 限制',
    file_too_large: '文件超过 20 MiB 限制',
    unsupported_type: '仅支持数字 PDF、TXT 或 Markdown',
    unsupported_scanned_pdf: 'PDF 没有可提取文字，v1 不支持扫描件',
    content_unreadable: '无法读取文件内容',
    filename_invalid: '文件名无效',
  };
  return messages[code] ?? '导入请求未完成，请检查连接后重试';
}

function validateFiles(files: readonly File[]): string | undefined {
  if (files.length > MAX_FILES) return 'batch_file_limit';
  if (files.some((file) => file.size > MAX_FILE_BYTES)) return 'file_too_large';
  if (files.reduce((total, file) => total + file.size, 0) > MAX_BATCH_BYTES) return 'batch_byte_limit';
  if (files.some((file) => !acceptedExtensions.has(file.name.split('.').pop()?.toLowerCase() ?? ''))) {
    return 'unsupported_type';
  }
  return undefined;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MiB`;
}

export function ImportView({ api = defaultApi, importEnabled = true }: ImportViewProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [course, setCourse] = useState<CourseSummary>();
  const [materials, setMaterials] = useState<MaterialSummary[]>([]);
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<DisplayResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [pageError, setPageError] = useState<{ code: string; retryable: boolean }>();

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const courses = await api.listCourses();
        const selected = courses[0] ?? await api.createCourse('操作系统', 'Asia/Shanghai');
        const existing = await api.listMaterials(selected.courseId);
        if (!active) return;
        setCourse(selected);
        setMaterials(existing);
      } catch (error) {
        if (!active) return;
        const requestError = error instanceof ApiRequestError ? error : undefined;
        setPageError({ code: requestError?.code ?? 'materials_unavailable', retryable: true });
      } finally {
        if (active) setLoading(false);
      }
    }
    void load();
    return () => { active = false; };
  }, [api]);

  function selectFiles(nextFiles: File[]) {
    const validationError = validateFiles(nextFiles);
    if (validationError) {
      setPageError({ code: validationError, retryable: false });
      return;
    }
    setFiles(nextFiles);
    setResults([]);
    setPageError(undefined);
  }

  function removeFile(index: number) {
    setFiles((current) => current.filter((_, fileIndex) => fileIndex !== index));
  }

  async function importSelected() {
    if (!course || files.length === 0 || uploading) return;
    setUploading(true);
    try {
      const response = await api.importMaterials(course.courseId, files);
      const displayResults = response.results.map((result, index) => ({
        ...result,
        filename: files[index]?.name ?? `文件 ${index + 1}`,
      }));
      setResults(displayResults);
      const firstFailure = displayResults.find((result) => result.errorCode);
      setPageError(firstFailure ? { code: firstFailure.errorCode!, retryable: firstFailure.retryable } : undefined);
      setMaterials(await api.listMaterials(course.courseId));
      if (!firstFailure) setFiles([]);
    } catch (error) {
      const requestError = error instanceof ApiRequestError || error instanceof Error
        ? error as Error & { code?: string; retryable?: boolean }
        : undefined;
      setPageError({
        code: requestError?.code ?? requestError?.message ?? 'import_failed',
        retryable: requestError?.retryable === true,
      });
    } finally {
      setUploading(false);
    }
  }

  const successCount = results.filter((result) => !result.errorCode).length;

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="page-title">
        <div>
          <p className="eyebrow">第 1 阶段 · 课程材料</p>
          <h1 id="page-title">导入课程材料</h1>
          <p className="introCopy">{importEnabled
            ? '原文件只保存在当前设备，导入后可逐页或逐行核对来源。'
            : 'Public demo materials are synthetic and isolated to this browser session.'}</p>
        </div>
        <p className={styles.courseName}><span>当前课程</span><strong>{course?.name ?? '操作系统'}</strong></p>
      </section>

      {importEnabled && <section className={styles.limits} aria-labelledby="limits-heading">
        <div>
          <h2 id="limits-heading">导入限制</h2>
          <p>仅支持含可提取文字的数字 PDF、TXT 或 Markdown；扫描件与图片暂不支持。</p>
        </div>
        <ul>
          <li>最多 5 个文件</li>
          <li>单文件 20 MiB</li>
          <li>本批合计 50 MiB</li>
        </ul>
      </section>}

      {pageError && (
        <section className={styles.error} role="alert">
          <AlertTriangle size={20} aria-hidden="true" />
          <div><strong>导入失败</strong><p>{errorMessage(pageError.code)}。{pageError.retryable ? '可以重试。' : '请调整文件后再试。'}</p></div>
        </section>
      )}

      <div className={styles.layout}>
        {importEnabled && <section aria-labelledby="select-heading">
          <div className={styles.sectionHeading}>
            <div><h2 id="select-heading">选择文件</h2><p>按所选顺序逐个处理，每个文件独立提交。</p></div>
          </div>
          <div className={styles.picker}>
            <Upload size={28} aria-hidden="true" />
            <p><strong>添加本机材料</strong><span>选择 PDF、TXT 或 Markdown 文件</span></p>
            <button type="button" className={styles.secondaryButton} title="选择材料文件" onClick={() => inputRef.current?.click()} disabled={uploading}>
              <Upload size={16} aria-hidden="true" />选择文件
            </button>
            <input
              ref={inputRef}
              className={styles.hiddenInput}
              type="file"
              multiple
              accept=".pdf,.txt,.md,application/pdf,text/plain,text/markdown"
              aria-label="选择材料文件"
              onChange={(event) => selectFiles(Array.from(event.target.files ?? []))}
            />
          </div>

          <div className={styles.selectionHeader}>
            <h3>已选文件</h3><span>{files.length} / 5</span>
          </div>
          {files.length === 0 ? <p className={styles.empty}>尚未选择文件。</p> : (
            <ul className={styles.fileList}>
              {files.map((file, index) => (
                <li key={`${file.name}-${file.lastModified}`}>
                  <FileText size={18} aria-hidden="true" />
                  <div><strong>{file.name}</strong><span>{formatSize(file.size)}</span></div>
                  <button type="button" title={`移除 ${file.name}`} aria-label={`移除 ${file.name}`} onClick={() => removeFile(index)} disabled={uploading}>
                    <X size={17} aria-hidden="true" />
                  </button>
                </li>
              ))}
            </ul>
          )}

          {uploading && <progress className={styles.progress} aria-label="导入进度">正在导入</progress>}
          <button type="button" className={styles.primaryButton} title="开始导入所选文件" onClick={() => void importSelected()} disabled={!course || files.length === 0 || uploading}>
            <Upload size={16} aria-hidden="true" />{uploading ? '正在导入…' : '开始导入'}
          </button>

          {results.length > 0 && (
            <section className={styles.results} aria-labelledby="results-heading">
              <h3 id="results-heading">逐文件结果</h3>
              {successCount > 0 && <p className={styles.successMessage} role="status"><CheckCircle2 size={17} aria-hidden="true" />已成功导入 {successCount} 个文件</p>}
              <ul>{results.map((result) => <li key={result.filename} className={result.errorCode ? styles.failedResult : styles.successResult}><strong>{result.filename}</strong><span>{result.errorCode ? errorMessage(result.errorCode) : '导入完成'}</span></li>)}</ul>
            </section>
          )}
        </section>}

        <section aria-labelledby="materials-heading">
          <div className={styles.sectionHeading}><div><h2 id="materials-heading">材料列表</h2><p>{materials.length} 份本地材料</p></div></div>
          {loading ? <p className={styles.empty} role="status">正在读取材料…</p> : materials.length === 0 ? <p className={styles.empty}>尚无材料。</p> : (
            <ul className={styles.materialList}>
              {materials.map((material) => (
                <li key={material.materialId}>
                  <FileText size={18} aria-hidden="true" />
                  <div><strong>{material.filename}</strong><span>{material.mediaType} · {material.status}</span></div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
