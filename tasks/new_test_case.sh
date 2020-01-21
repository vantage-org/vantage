#!/bin/sh
# ---
# help-text: Creates a new test case
# ---
set -e
if [ -z "$1" ]; then
    echo "You must provide a test case name. e.g. task/container_task_inherits_env"
    exit 1
fi
(
    cd "$VG_APP_DIR/tests/cases"
    if [ -d "$1" ]; then
        echo "A test with this name already exists"
        exit 2
    fi
    mkdir -p "$1"
    cd "$1"

    cat > run.sh<<EOF
#!/bin/sh
vantage do-something
EOF
    chmod +x run.sh

    NAME=$(basename "$1")
        cat > "test_$NAME.py"<<EOF
def test_$NAME(stdout, stderr):
    assert False
EOF

    mkdir -p tasks
    cat > tasks/do-something<<EOF
#!/bin/sh
echo 'something!'
EOF
    chmod +x tasks/do-something
)
