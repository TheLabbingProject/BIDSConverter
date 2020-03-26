# YA_Colab Code

# BidsConvert module:
Create, manipulate, validate and present a BIDS compliant directory.

## Class BidsGenerator
Contains several functions aimed at generating the main sub directories for the BIDS compliant dataset. (i.e, converting the raw dicom files to BIDS-sorted niftis)

>>        """
>>        Initialize a class that creates/validates/presents a BIDS compliant directory.
>>        Arguments:
>>            raw {str} -- Path to a directory that contains the raw dicom files. (sourcedata)
>>            bids_dir {str} -- Path to the directory to initialize as a BIDS compliant one.
>>        """

### Usage:
```
>>> from Code import BidsConvert

>>> gen_bids = BidsConvert.BidsGenerator(
        bids_dir = '/path/to/your/bids_dir',
        raw = '/path/to/your/raw_data')
```
* Note that the raw directory should contain subdirectories with name such as "sub-XX"
```
>>> gen_bids.run()
```
### Output:
A BIDS compliant directory, containing the niftis converted from the raw dicom directory.

* bids_dataset/
    * sub-01/
        * dwi/
            * sub-01_acq-AP_dwi.bvec
            * sub-01_acq-AP_dwi.nii
            * sub-01_acq-AP_dwi.bval
            * sub-01_acq-AP_dwi.json
        * fmap/
            * sub-01_acq-PA_dwi.nii
            * sub-01_acq-PA_dwi.json
        * anat/
            * sub-01_acq-T1w.nii
            * sub-01_acq-T2w.json
            * sub-01_acq-T2w.nii
            * sub-01_acq-T1w.json
        * func/
            * sub-01_task-rest_bold.nii
            * sub-01_task-rest_sbref.nii
            * sub-01_task-rest_sbref.json
            * sub-01_task-rest_bold.json
    * sub-02/
    * .
    * .
    * .


## Class FilesGenerator
Contains several functions aimed at generating BIDS compliant dataset descriptive files. (i.e, dataset_description.json and participants.tsv)

* Note that this class does not create the recommended README file, as it should be manually created by the researcher.

>>>        """
>>>        Generate BIDS compliant dataset description file and participants file (based on a template and CRF file)
>>>        Arguments:
>>>            bids_dir {str} -- Path to the directory to initialize as a BIDS compliant one.
>>>            subj_temp {str} -- Participant template file as can be obtained from https://github.com/bids-standard/bids-starter-kit/tree/master/templates
>>>            crf {str} -- A CRF files containing data regarding the participants in the dataset.
>>>            ds_temp (str) -- Path to a dataset description template as can be obtained from https://github.com/bids-standard/bids-starter-kit/tree/master/templates
>>>        """

### Usage:
```
>>> from Code import BidsConvert
>>> gen_files = BidsConvert.Generate_Files(
        bids_dir = '/path/to/your/bids_dir',
        subj_temp = '/path/to/paticipants_template.tsv',
        crf = '/path/to/CRF.xlsx',
        ds_temp = '/path/to/dataset_description.json)

>>> gen_files.run()
```
### Output:
The dataset descriptive files, as demended by the BIDS specifications.

* bids_dataset/
    * dataset_description.json
    * participants.tsv

dataset_description.json:
```
{
    "Name": "[Name of your bids dataset directory]",
    "BIDSVersion": "1.0.2",
    "License": "",
    "Authors": [
        "",
        "",
        ""
    ],
    "Acknowledgements": "",
    "HowToAcknowledge": "",
    "Funding": [
        "",
        "",
        ""
    ],
    "ReferencesAndLinks": [
        "",
        "",
        ""
    ],
    "DatasetDOI": ""
}
```

participants.tsv:
| participant_id  | age | handedness | sex |
| ------------- | ------------- | ------------- | -------------|
| sub-01  | 18  | r | m |
| sub-02  | .  | . | . |
| .
| .
| .
