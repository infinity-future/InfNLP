
rm -rf ./dist
rm -rf ./build
rm -rf ./*.egg-info
python3 setup.py bdist_wheel
twine upload dist/*.whl
