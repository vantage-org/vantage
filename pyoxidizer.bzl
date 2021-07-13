
def make_dist():
    return default_python_distribution()

def make_exe(dist):
    policy = dist.make_python_packaging_policy()
    policy.resources_location_fallback = "filesystem-relative:lib"

    python_config = dist.make_python_interpreter_config()

    python_config.run_command = "from vantage.entry import vantage; vantage()"
    exe = dist.to_python_executable(
        name="vantage",
        packaging_policy=policy,
        config=python_config,
    )

    for resource in exe.pip_install([CWD]):
        resource.add_location = "in-memory"
        exe.add_python_resource(resource)

    return exe

def make_embedded_resources(exe):
    return exe.to_embedded_resources()

def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)

    return files

def make_msi(exe):
    return exe.to_wix_msi_builder(
        # Simple identifier of your app.
        "vantage",
        # The name of your application.
        "vantage",
        # The version of your application.
        "3.2.0",
        # The author/manufacturer of your application.
        "William Mayor"
    )


def register_code_signers():
    if not VARS.get("ENABLE_CODE_SIGNING"):
        return


register_code_signers()

register_target("dist", make_dist)
register_target("exe", make_exe, depends=["dist"])
register_target("resources", make_embedded_resources, depends=["exe"], default_build_script=True)
register_target("install", make_install, depends=["exe"], default=True)
register_target("msi_installer", make_msi, depends=["exe"])


resolve_targets()

PYOXIDIZER_VERSION = "0.16.2"
PYOXIDIZER_COMMIT = "e91995636f8deed0a7d8e1917f96a7dc17309b63"
