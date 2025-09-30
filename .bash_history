git update-index --chmod=+x .render-build.sh
git add .render-build.sh
git update-index --chmod=+x .render-build.sh
git commit -m "fix(backend): Add build script and enhanced logging"
git push origin master
git add backend/main.py
git commit -m "fix(backend): Add regex for Lightning AI to CORS origins"
git push origin master
git add backend/main.py
git commit -m "perf(backend): Add detailed timing logs to debug latency"
git push origin master
