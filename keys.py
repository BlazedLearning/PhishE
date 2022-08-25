#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Configuration

misp_url = Configuration.MISP_URL() # The MISP instance URL
misp_key = Configuration.MISP_Key() # The MISP auth key can be found on the MISP web interface under the automation section
misp_verifycert = False
misp_client_cert = ''
proofpoint_sp = '<proofpoint service principal>'  # Service Principal from TAP (https://threatinsight.proofpoint.com/<custID>/settings/connected-applications)
proofpoint_secret = '<proofpoint secret>'
