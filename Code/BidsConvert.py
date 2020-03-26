import glob, os
import dicom_parser
import pandas as pd
import json


class BidsGenerator:
    """
    Create, manipulate, validate and present a BIDS compliant directory.
    """

    def __init__(self, bids_dir: str, raw: str):
        """
        Initialize a class that creates/validates/presents a BIDS compliant directory.
        Arguments:
            raw {str} -- Path to a directory that contains the raw dicom files. (sourcedata)
            bids_dir {str} -- Path to the directory to initialize as a BIDS compliant one.
        """
        self.bids_dir = bids_dir
        self.raw = raw
        if not os.path.isdir(bids_dir):
            print("Creating BIDS mother dir...")
            os.mkdir(bids_dir)
        if not os.listdir(bids_dir):
            print(f"Initializing BIDS directory at {bids_dir}...")
            self.init_bids_dir(self.raw, self.bids_dir)

    def list_files(self, startpath: str):
        """
        Print a summary of directory's tree
        Arguments:
            startpath {str} -- A path to a directory to inspect
        """
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, "").count(os.sep)
            indent = " " * 4 * (level)
            print("{}{}/".format(indent, os.path.basename(root)))
            subindent = " " * 4 * (level + 1)
            for f in files:
                if ".DS_Store" not in f:
                    print("{}{}".format(subindent, f))

    def init_bids_dir(self, raw: str, bids_dir: str):
        """
        Initialize the main directories that need to conduct the BIDS compiant mother directory.
        Arguments:
            raw {str} -- Path to raw data (dicom) dir.
            bids_dir {str} -- Path to BIDS directory.
        """
        acqs = ["anat", "fmap", "func", "dwi"]
        for subj in os.listdir(raw):
            os.mkdir(f"{bids_dir}/{subj}")
            for subdir in acqs:
                os.mkdir(f"{bids_dir}/{subj}/{subdir}")
        print(f"Created a bids-like directory tree at {bids_dir}")
        self.list_files(bids_dir)

    def get_raw_acq(self, dcm_dir: str):
        """
        Use dicom_parser functionalities to detect acqusitions used to extract the raw data.
        Arguments:
            dcm_dir {str} -- Path to a directory that contains dicom files.

        Returns:
            acq (str) -- The acquisition used to extract the raw data found in the directory in hand.
        """
        cur_dir = os.getcwd()
        os.chdir(dcm_dir)
        header = dicom_parser.Header(os.listdir(dcm_dir)[0])
        acq = header.detect_sequence()
        os.chdir(cur_dir)
        return acq

    def convert_dcm(self, dcm_dir: str, bids_dir: str):
        """
        Convert raw dicom to nifti in the correct target dir according to BIDS specifications.
        Arguments:
            dcm_dir {str} -- Path to a directory that contains dicom files.
            bids_dir {str} -- Path to BIDS directory.
        """
        subj = dcm_dir.split(os.sep)[-2]
        acq = self.get_raw_acq(dcm_dir)
        output = self.get_output(dcm_dir, acq, subj, bids_dir)
        if output:
            f_name = output.split(os.sep)[-1]
            d_name = os.path.dirname(output)
            if not os.path.isdir(d_name):
                os.makedirs(d_name)
            cmd = f"dcm2niix -o {d_name} -f {f_name} {dcm_dir}"
            print(cmd)
            os.system(cmd)

    def get_output(self, dcm_dir: str, acq: str, subj: str, bids_dir: str):
        """
        Toggle the dicom dir's name, acq as extracted using dicom_parser and subject's id to define the corresponding output nifti file.
        Arguments:
            dcm_dir {str} -- Path to a directory that contains dicom files.
            acq {str} -- Acquistion as extracted using dicom_parser
            subj (str) -- Subject's id (sub-xx)
            bids_dir (str) -- Path to BIDS directory.
        Returns:
            ouotput (str or None) - Correct nifti file to be used as target for conversion in order to compile to BIDS specification.
        """
        if acq == "mprage":
            output = f"{bids_dir}/{subj}/anat/{subj}_acq-T1w"
        elif acq == "flair":
            output = f"{bids_dir}/{subj}/anat/{subj}_acq-T2w"
        elif acq == "ep2d":
            if "AP" in dcm_dir:
                output = f"{bids_dir}/{subj}/dwi/{subj}_acq-AP_dwi"
            elif "PA" in dcm_dir:
                output = f"{bids_dir}/{subj}/fmap/{subj}_acq-PA_dwi"
            else:
                output = None
        elif acq == "fmri":
            if "SBRef" in dcm_dir:
                output = f"{bids_dir}/{subj}/func/{subj}_task-rest_sbref"
            else:
                output = f"{bids_dir}/{subj}/func/{subj}_task-rest_bold"
        else:
            output = None
        return output

    def run(self):
        """
        Generate a BIDS compiant directory based on a raw data (dicom) directory.
        """
        dcm_dirs = glob.glob(f"{self.raw}/*/*")
        dcm_dirs.sort()
        for dcm_dir in dcm_dirs:
            if os.path.isdir(dcm_dir):
                self.convert_dcm(dcm_dir, self.bids_dir)
        self.list_files(self.bids_dir)


class FilesGenerator:
    def __init__(self, bids_dir: str, subj_temp: str, crf: str, ds_temp: str):
        """
        Generate BIDS compliant dataset description file and participants file (based on a template and CRF file)
        Arguments:
            bids_dir {str} -- Path to the directory to initialize as a BIDS compliant one.
            subj_temp {str} -- Participant template file as can be obtained from https://github.com/bids-standard/bids-starter-kit/tree/master/templates
            crf {str} -- A CRF files containing data regarding the participants in the dataset.
            ds_temp (str) -- Path to a dataset description template as can be obtained from https://github.com/bids-standard/bids-starter-kit/tree/master/templates
        """
        self.bids_dir = bids_dir
        self.subj_temp = subj_temp
        self.ds_temp = ds_temp
        self.crf = crf

    def participants(
        self,
        sub: str,
        age: str,
        hand: str,
        sex: str,
        participant_tsv: str,
        temp_participants: str,
    ):
        """
        Add participant to participants file
        Arguments:
            sub {str} -- Subject's id (sub-xx).
            age {str} -- Subject's age.
            hand {str} -- Subject's dominant hand (either 'r' or 'l')
            sex {str} -- Subject's sex (either 'm' or 'f')
            participant_tsv {str} -- Dataset's participants description file.
            temp_participants {str} -- Participant's description template file (from bids starter kit)
        """
        if not os.path.isfile(participant_tsv):
            df = pd.read_csv(temp_participants, sep="\t")
        else:
            df = pd.read_csv(participant_tsv, sep="\t")
        loc = int(sub[-2:])
        if not loc in df["participant_id"].values:
            newline = [sub, age, hand, sex]
            df.loc[loc - 1] = newline
            df.to_csv(participant_tsv, sep="\t", index=False)
            print(f"Added sub-{sub} to participants.tsv")
        else:
            print(f"sub-{sub} is already a part of this dataset")

    def dataset_description(self, ds_description: str, Proj_Name: str = None):
        """
        Create BIDS` dataset description file.
        Arguments:
            ds_description {str} -- Dataset description template file.
        """
        if not Proj_Name:
            Proj_Name = self.bids_dir.split(os.sep)[
                -1
            ]  # Define project name as it will be in the .json file
        replacements = {"proj_name": Proj_Name}
        #        if os.path.isfile(
        #            "{0}/dataset_description.json".format(os.path.dirname(new_toplvl))
        #        ):
        with open(ds_description, "r") as infile:
            with open(f"{self.bids_dir}/dataset_description.json", "w") as outfile:
                # for line in infile:
                #     for src, target in replacements.items():
                #         line = line.replace(src, target)
                #     outfile.write(line)
                ds_temp = json.load(infile)
                ds_temp["Name"] = Proj_Name
                json.dump(ds_temp, outfile, indent=4)
        print("Created dataset_description.json")

    def run(self):
        """
        Generate dataset's main descriptive files.
        """
        subjects = glob.glob(f"{self.bids_dir}/sub-*")
        subjects.sort()
        df = pd.read_excel(self.crf, header=0)
        for subj in subjects:
            subnum = subj.split(os.sep)[-1]
            print(f"Adding {subnum} to project`s database...")
            data = df.iloc[int(subnum.split("-")[-1]) - 1]
            identifier = str(data["subnum"].split("-")[-1])
            age = data.Age
            hand = data.Hand
            sex = data.Gender
            self.participants(
                sub=identifier,
                age=age,
                hand=hand,
                sex=sex,
                participant_tsv=f"{self.bids_dir}/participants.tsv",
                temp_participants=self.subj_temp,
            )
        self.dataset_description(ds_description=self.ds_temp)
