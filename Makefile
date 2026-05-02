.PHONY: all install run clean

all: install run

install:
	pip install -r requirements.txt

run:
	jupyter nbconvert --to notebook --execute --inplace code/data_cleaning/data_cleaning.ipynb
	jupyter nbconvert --to notebook --execute --inplace code/model/cosine_model.ipynb
	jupyter nbconvert --to notebook --execute --inplace code/model/knn_model.ipynb

clean:
	find . -name "*.ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
