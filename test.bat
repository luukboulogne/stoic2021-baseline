call .\build.bat

docker volume create stoicalgorithm-output

docker run --rm --gpus all^
 --memory=16g --memory-swap=16g^
 --cap-drop=ALL --security-opt="no-new-privileges"^
 --network none --shm-size=128m --pids-limit 256^
 -v %~dp0\test\:/input/^
 -v stoicalgorithm-output:/output/^
 stoicalgorithm

docker run --rm^
 -v stoicalgorithm-output:/output/^
 python:3.7-slim cat /output/probability-covid-19.json | python -m json.tool

docker run --rm^
 -v stoicalgorithm-output:/output/^
 python:3.7-slim cat /output/probability-severe-covid-19.json | python -m json.tool

docker run --rm^
 -v stoicalgorithm-output:/output/^
 -v %~dp0\test\:/input/^
 python:3.7-slim python -c "import json, sys; f1a = json.load(open('/output/probability-covid-19.json')); f2a = json.load(open('/input/expected_output-probability-covid-19.json')); f1b = json.load(open('/output/probability-severe-covid-19.json')); f2b = json.load(open('/input/expected_output-probability-severe-covid-19.json')); sys.exit((f1a != f2a)|(f1b != f2b));"

if %ERRORLEVEL% == 0 (
	echo "Tests successfully passed..."
)
else
(
	echo "Expected output was not found..."
)

docker volume rm stoicalgorithm-output
