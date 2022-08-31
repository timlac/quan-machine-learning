# emotional-recognition

## Running code in src
In order for imports to work correctly modules should be run with the `-m` flag. [Read more](https://docs.python.org/3.8/using/cmdline.html#cmdoption-m)
### Create dataset 

```bash
python -m src.preprocessing.dataset_creation.create_functionals_ds
```

### Run grid search
```bash
python -m src.analysis.supervised_learning.param_search.svm
```