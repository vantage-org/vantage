from pathlib import Path


def test_uninstall(workdir, run):
    plugin = Path(workdir) / ".vg-plugins" / "fake"
    assert plugin.is_dir()
    run()
    assert not plugin.is_dir()
