.PHONY: all install run clean

all: install run

install:
	pip install -r requirements.txt

run:
	cd code/data_cleaning && jupyter nbconvert --to notebook --execute --inplace data_cleaning.ipynb
	cd code/model && jupyter nbconvert --to notebook --execute --inplace cosine_model.ipynb
	cd code/model && jupyter nbconvert --to notebook --execute --inplace knn.ipynb
	cd code/model && jupyter nbconvert --to notebook --execute --inplace xgboost.ipynb

clean:
	find . -name "*.ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
