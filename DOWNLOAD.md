Dataset **Mattings Human** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMxMjNfTWF0dGluZ3MgSHVtYW4vbWF0dGluZ3MtaHVtYW4tRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAibDhnalhQQTZLZkl5dHc5MklxM2x0YkhqcjZ0eHVqcS9xYUFJNUIrNktkcz0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Mattings Human', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/laurentmih/aisegmentcom-matting-human-datasets/download?datasetVersionNumber=1).