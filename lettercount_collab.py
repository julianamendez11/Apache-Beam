pip install --quiet apache-beam

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

def run(cmd):
  print('>> {}'.format(cmd))
  !{cmd}
  print('')
  
#para contar las palabras o letras de todos los archivos .txt que estén adentro de la carpeta /content
inputs_pattern = '/content/*'
outputs_prefix = '/content'

with beam.Pipeline() as pipeline:
  (
      pipeline
      | 'Read lines' >> beam.io.ReadFromText(inputs_pattern)
      | 'Find words' >> beam.FlatMap(lambda line: re.findall("[a-zA-Z']", line))
      | 'Pair words with 1' >> beam.Map(lambda word: (word, 1))
      | 'Group and sum' >> beam.CombinePerKey(sum)
      | 'Format results' >> beam.Map(lambda word_count: str(word_count))
      | 'Write results' >> beam.io.WriteToText(outputs_prefix)
  )

# Sample the first 20 results, remember there are no ordering guarantees.
run('head -n 20 {}-00000-of-*'.format(outputs_prefix))
