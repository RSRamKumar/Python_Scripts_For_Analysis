import logging
import os.path
import time

import pandas as pd
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db import transaction
import urllib

from variantmanagement.variantdata.models import *
from variantmanagement.variantdata.utils import get_vep_data_by_hgvs

logger = logging.getLogger(__name__)
project_dir = (os.getcwd())

log_dir = os.path.join(project_dir,'logs')
os.makedirs(log_dir,exist_ok=True)

log_file_path = os.path.join(log_dir,'create_variantversion_hg38_log.log')

logging.basicConfig(filename=log_file_path,
                    format = '%(asctime)s -%(name)s - %(levelname)s -%(message)s',
                    level = logging.DEBUG,  force = True )

def retry(func, retry = 2):
    """
    wrapper function for retrying an API request
    :param func:
    :param retry: number of retry attempts
    :return: response / error message
    """

    def retry_wrapper(*args, **kwargs):
        attempt  = 0
        while attempt < retry:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as error:
                logger.warning('Made a retry....')
                time.sleep(2)
                attempt += 1
    return retry_wrapper

@retry
def assembly_converter(chromosome, start_pos, stop_pos):
    """
    convert hg19 to hg38 coordinates
    :param chromosome: chromosome number
    :param start_pos: start coordiantes of the variation
    :param stop_pos: stop coordiantes of the variation
    :return: new Hg38 coordiantes / error messages
    """
    chromosome, start_pos, stop_pos = str(chromosome), str(start_pos), str(stop_pos)

    # changing the chromosome number 23 and 24 as X and Y respectively
    sex_chr = {'23': 'X', '24': 'Y'}
    chromosome = sex_chr[chromosome] if chromosome in sex_chr else chromosome

    api_url = "https://rest.ensembl.org/map/human/GRCh37/{}:{}..{}/GRCh38?".format(chromosome, start_pos, stop_pos)
    r = requests.get(api_url, headers={"Content-Type": "application/json"})
    #print(r.raise_for_status())
    response = r.json()['mappings']

    if len(response) == 0: #'Ensembl has no mapping for this coordinates'
        return None, None
    elif len(response) == 1: # clear ones
        mapped = response[0]['mapped']
        return mapped['start'], mapped['end']
    else: # 'Ensembl has no clear response for this coordinates'
        return None, None


@retry
def get_hgvs_hg38(hgvs_id):
    """
    Replicates the Mutalyzer - Position converter tool
    :param hgvs_id: hg19 variant
    :return: hg38 variant / error message
    """

    def find_transcripts(soup):
        try:
            transcripts_list_raw = list(
                soup.find(text="Found transcripts in variant region").findNext('pre').stripped_strings)
            transcripts = []
            for index, raw_trans in enumerate(transcripts_list_raw):
                raw_trans_unedited = transcripts_list_raw[index].replace('\n', ',').split('\t')
                raw_trans_edited = [i.strip(',') for i in raw_trans_unedited if i and i[-1] != ':']
                transcripts.extend(raw_trans_edited)
                # print(transcripts)
            return transcripts

        except Exception:
            return None


    def find_chromosomal_variants(soup):
        try:
            variant = soup.find(text="Chromosomal variant").findNext('p').text
            return variant
        except Exception:
            return None

    def getting_details_for_grch37(hgvs_id):
        response = requests.get(
            'https://mutalyzer.nl/position-converter?assembly_name_or_alias=GRCh37&description={}'.format(hgvs_id))
        soup = BeautifulSoup(response.text, "html.parser")
        grch37_transcripts = find_transcripts(soup)
        return grch37_transcripts

    def getting_hgvs_grch38(hgvs_id):
        grch37_transcripts = getting_details_for_grch37(hgvs_id)
        if grch37_transcripts == None:
            return 'ID not possible / available'
        else:
            hgvs_grch38_id = None
            for trans in grch37_transcripts:
                trans = urllib.parse.quote(trans)
                response = requests.get(
                    'https://mutalyzer.nl/position-converter?assembly_name_or_alias=GRCh38&description={}'.format(
                        trans))
                soup = BeautifulSoup(response.text, "html.parser")
                hgvs_grch38_id = find_chromosomal_variants(soup)

                if (hgvs_grch38_id != None) :
                    return hgvs_grch38_id

        return hgvs_grch38_id if hgvs_grch38_id else 'No variant ID obtained even after trying all transcripts'


    return getting_hgvs_grch38(hgvs_id)



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with transaction.atomic():

            # retrieving the variant data, custom code

            variant_data = Variantversion.objects.all()
            result_list = []

            sex_chr = {23: 'X', 24: 'Y'}

            s = requests.Session() # creating a new session

            for var in variant_data[:51] :


                # changing the chromosomes and linking for foreign key
                chro_symbol_19 = var.chromosome_id if var.chromosome_id not in sex_chr else sex_chr[var.chromosome_id]

                chr_hg38_for_current_variant_version = Chromosome.objects.get(referencegenome=2, symbol=chro_symbol_19)


                # Obtaining results
                logger.info('***** Variant ID in the process now is {} *********'.format(var))
                hg38_coordinates  = assembly_converter(var.chromosome, var.genomic_location_start , var.genomic_location_end)
                hgvs_genomic_hg38_id = get_hgvs_hg38(var.hgvs_genomic)
                vcf_string_hg38 = get_vep_data_by_hgvs(hgvs_genomic_hg38_id, params={'vcf_string':1}).get('vcf_string', None)
                logger.info('***** Completed ID is {} *********'.format(var))


                # try:
                #    current_vv_hg38 = Variantversion.objects.get(hgvs_genomic=hgvs_genomic_hg38_id)
                # except Variantversion.DoesNotExist :
                #    current_vv_hg38 = Variantversion(
                #        genomic_location_end=hg38_coordinates[1] if type(hg38_coordinates) == tuple else None,
                #        genomic_location_start=hg38_coordinates[0] if type(hg38_coordinates) == tuple else None,
                #        hgvs_genomic=hgvs_genomic_hg38_id,
                #        chromosome=chr_hg38_for_current_variant_version,
                #        vcf_string=vcf_string_hg38,
                #        variant=var.variant)
                #
                # current_vv_hg38.save()
                # logger.info('The variant ID {} is saved in the database successfully'.format(current_vv_hg38.id))

                #converting into a dict for writing a csv (for viewing the results)
                result_dict = {
                    'id': var,
                    'hgvs_genomic': hgvs_genomic_hg38_id,
                    'genomic_location_end': hg38_coordinates[0] if type(hg38_coordinates) == tuple else None,
                    'genomic_location_start': hg38_coordinates[1] if type(hg38_coordinates) == tuple else None,
                    'vcf_string': vcf_string_hg38,
                    'chromosome': chr_hg38_for_current_variant_version

                }
                result_list.append(result_dict)

            df = pd.DataFrame(result_list)
            df.to_csv('results_hg38.csv', index=False, na_rep=None)






























#https://stackoverflow.com/questions/30861524/logging-basicconfig-not-creating-log-file-when-i-run-in-pycharm


