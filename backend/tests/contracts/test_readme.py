from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
README = ROOT / "README.md"


def test_readme_records_required_delivery_contract_without_false_completion_claims() -> None:
    text = README.read_text(encoding="utf-8")
    for heading in (
        "# ProjectB",
        "## 功能模块",
        "## 安装与开发运行",
        "## 测试",
        "## Windows 单文件分发",
        "## OCI 本地演示",
        "## 安全与凭据",
        "## 目录结构",
        "## CI/CD",
        "## 第三方依赖与许可证",
        "## 已知限制与交付状态",
    ):
        assert heading in text

    for literal in (
        "python scripts/test_all.py",
        "packaging/windows/build.ps1",
        "docker build --platform linux/amd64 --file packaging/oci/Dockerfile",
        "Windows Credential Manager",
        "127.0.0.1",
        "Python 3.14.6",
        "Node.js 24.18.0",
        "npm 11.16.0",
        ".gitlab-ci.yml",
        "unit-test",
        "licenses/THIRD_PARTY_NOTICES.md",
    ):
        assert literal in text

    assert "干净 Windows VM 的 10 秒启动门槛尚未通过" in text
    assert "公网部署已按项目决策豁免" in text
    assert "远端 GitLab/GitHub CI 尚未执行" in text
    assert "CI 已全部通过" not in text
    assert "正式发布已完成" not in text
