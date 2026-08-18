for py in 3.10 3.11 3.12 3.13 3.14; do
  conda create -y -n "activestorage-$py" python=$py \
    pyactivestorage moto pytest pytest-cov pytest-html pytest-metadata pytest-xdist \
    -c conda-forge
done
