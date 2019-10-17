from pathlib import Path


def test_creates_vantage_file(tmpdir, run):
    run()
    tmpdir = Path(tmpdir)
    vg_file = tmpdir / "case" / ".vantage"
    assert vg_file.is_file()
    with vg_file.open() as fp:
        contents = [c.strip() for c in fp.readlines()]
        assert f"VG_TASKS_DIR={tmpdir}/case/tasks" in contents
        assert f"VG_PLUGINS_DIR={tmpdir}/case/.vg-plugins" in contents
        assert f"VG_ENV_DIR={tmpdir}/case/.env" in contents
        assert "VG_DEFAULT_ENV=default" in contents


def test_creates_default_env(tmpdir, run):
    run()
    tmpdir = Path(tmpdir)
    env_dir = tmpdir / "case" / ".env"
    assert env_dir.is_dir()
    env_file = env_dir / "default"
    assert env_file.is_file()
