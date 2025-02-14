if ! command -v docker > /dev/null; then
    if ! command -v podman > /dev/null; then
        echo 'Docker or podman not found'
        exit 1
    fi
    alias docker="podman"
fi
trap "exit" INT
shopt -s expand_aliases
mkdir -p docs
docker build --target docs-0 -t taskmgmt_server_docs_0 .
docker run --env-file "$1" --rm -v "$(pwd)/docs:/app/docs:z" taskmgmt_server_docs_0
docker build --target docs -t taskmgmt_server_docs .
docker run --rm -v "$(pwd)/docs:/app:z" taskmgmt_server_docs
