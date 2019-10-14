from pathlib import Path


def test_install_official(tmpdir, run):
    run()
    plugin = Path(tmpdir) / "case" / ".vg-plugins" / "pg"
    assert plugin.is_dir()
