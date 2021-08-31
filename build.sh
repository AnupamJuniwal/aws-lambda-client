# clear old build data
echo "============ Cleaning ============"
rm -rf *.egg-info
rm -rf build/*
rm -rf dist/* 

# create build
echo "============ Building ============"
python setup.py bdist_wheel  

echo "=========== Uploading ============"
python -m twine upload dist/*