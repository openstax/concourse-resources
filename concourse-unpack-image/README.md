# Concourse unpack image

An image for Concourse tasks that unpack an image tarball into the `rootfs/` and
`metadata.json` format that a task's `image:` needs. It's Alpine with `crane` and `jq`.

unified-deployment's `concourse/unpack-image` task runs in it.

## Building

```bash
docker build --platform linux/amd64 -t openstax/concourse-unpack-image:TAG .
docker push openstax/concourse-unpack-image:TAG
```

Use the date as the tag, such as `2026-11-24`, and pin that tag in the tasks that use it.
