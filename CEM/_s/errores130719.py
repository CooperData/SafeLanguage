#!/home/ascander/py3/Python-3.3.1/python
# -*- coding: utf-8  -*-
import sys, getopt, re
import excluidos

url = re.compile('(?i)(?:(?:https?|mailto)://[\w@/%.\-_?&=:;\'\~+,()#]+)')
reg = re.compile('_')                                                        
def lemaB(pat,src, pres='',posts=''):
    """match patterns"""                                                        
    #print "Wrong pattern: %s" % (pat)                                          
    p = reg.split(pat)
    if len (p) < 4:
        print ("Wrong pattern: %s" % (pat))
        #raise LemaExc(pat)                                                     
    if len (p) == 5:
        fl = '(?i)'
    else:
        fl = ''
    #Contexts                                                                   
    # url: '(?<!http:[\w/\-_%?&=(),]+)'                                       
    # interwiki:(?!\[\[\w+\:[^\[\]]*)                                           
    #return [(fl + '([^\w/áéíóúñÁÉÍÓÚÑ]' + p[0] + ')' + p[3] +              
    #        '(' + p[2] + '[^\w/áéíóúñÁÉÍÓÚÑ])',                            
    #        '\1' + p[1] + '\2')]                                           
    res =( [ [pres+p[0] + p[3] + p[2]+posts, src, 0] ])
    #print (res)
    return res
alpha = '[a-zæǣçäëöüãâêàèìòùáéíóúñžŕA-ZÆÇÄËÖÜÃÂÊÀÈÌÒÙÁÉÍÓÚÑŽŔß_/ÐðŜŝĒēŠšÏïÞþÔ\
ôÕõŁłŌōŢţ]'

qte = re.compile("[']")
def lema(pat, pre=None, post=None):
  src = "lema(ur\'"+qte.sub("\\'",pat)+"\'"
  pres=''
  if not pre is None:
      src+=", pre=["
      for p in pre:
          pres += "(?<!"+p+")"
          src+="ur\'"+qte.sub("\\'",p)+"\', "
      src+="]"
  posts=''
  if not post is None:
      src+=", post=["
      for p in post:
          posts += "(?!"+p+")"
          src+="ur\'"+qte.sub("\\'",p)+"\', "
      src+="]"
  src+=") + "
  print (src)
  #print(pat)
#  return lemaB(pat,'(?<!' + alpha + ')(', ')(?!' + alpha + ')')
  return lemaB(pat,src, pres,posts)
def retro(pat):
  return []

lemas = [

#lema(ur"_Crimen & Investigación (España)__Crimen & Investigacion Network \(España\)_x") + #Cambio de nombre
lema('[Aa]__compañará_a') + 
lema('[Aa]_sis_tirá_isi') + 
lema('[Aa]bati_ó__o') + 
lema('[Aa]bri_ó__o') + 
lema('[Aa]burri_ó__o') + 
lema('[Aa]c__ompañará_c') + 
lema('[Aa]c_e_ptará_') + 
lema('[Aa]cab_a_rá_') + 
lema('[Aa]co_g_erá_j') + 
lema('[Aa]compa_ña_rá_rá') + 
lema('[Aa]cudi_ó__o') + 
lema('[Aa]dem_á_s_a') + 
lema('[Aa]dmiti_ó__o') + 
lema('[Aa]dscribi_ó__o') + 
lema('[Aa]lbe_r_gará_') + 
lema('[Aa]ll_í__i', pre=['Yusuf ', 'Jiménez ', 'Cruz '], post=[' [Ll]ettori']) + 
lema('[Aa]ludi_ó__o') + 
lema('[Aa]men_a_zará_') + 
lema('[Aa]ntinarc_ó_ticos?_o') + 
lema('[Aa]par_e_cerá_') + 
lema('[Aa]percibi_ó__o') + 
lema('[Aa]prendi_ó__o') + 
lema('[Aa]plaudi_ó__o') + 
lema('[Aa]pr_o_vechará_') + 
lema('[Aa]sis__tieron_i') + 
lema('[Aa]sisti_ó__o') + 
lema('[Aa]sumi_ó__o') + 
lema('[Aa]turdi_ó__o') + 
lema('[Aa]ñadi_ó__o') + 
lema('[Bb]_ri_tánic[ao]s?_ir') + 
lema('(?<!Angelo )[Bb]ati_ó__o') + 
lema('[Cc]ircunscribi_ó__o') + 
lema('[Cc]oescribi_ó__o') + 
lema('[Cc]oexisti_ó__o') + 
lema('[Cc]oincidi_ó__o') + 
lema('[Cc]ombati_ó__o') + 
lema('[Cc]omenz_ó__o') + 
lema('[Cc]omparti_ó__o') + 
lema('[Cc]on_s_truyeron_') + 
lema('[Cc]oncurri_ó__o') + 
lema('[Cc]onfundi_ó__o') + 
lema('[Cc]ons_i_guieron_e') + 
lema('[Cc]onsisti_ó__o') + 
lema('[Cc]onsumi_ó__o') + 
lema('[Cc]onvi__rtieron_e') + 
lema('[Cc]onvi_r_tieron_') + 
lema('[Cc]ubri_ó__o') + 
lema('[Cc]umpli_ó__o') + 
lema('[Cc]undi_ó__o') + 
lema('[Dd]_e_cidió_i') + 
lema('[Dd]e__cidió_i') + 
lema('[Dd]ebati_ó__o') + 
lema('[Dd]eci__dió_ci') + 
lema('[Dd]ecidi_ó_(?! Saxa)_o') + 
lema('[Dd]ef__endió_i') + 
lema('[Dd]efini_ó__o') + 
lema('[Dd]escribi_ó__o') + 
lema('[Dd]escub_r_ieron_') + 
lema('[Dd]escubri_ó__o') + 
lema('[Dd]esisti_ó__o') + 
lema('[Dd]esp_i_dió_e') + 
lema('[Dd]_espué_s_(?:espue|epue|epué)') + 
lema('[Dd]etr_á_s_a') + 
lema('[Dd]i_o__ó') + 
lema('[Dd]ifundi_ó__o') + 
lema('[Dd]imiti_ó__o') + 
lema('[Dd]irimi_ó__o') + 
lema('[Dd]iscurri_ó__o') + 
lema('[Dd]iscuti_ó__o') + 
lema('[Dd]isuadi_ó__o') + 
lema('[Dd]ividi_ó__o') + 
lema('[Ee]l_e_girá[ns]?_i') + 
lema('[Ee]ludi_ó__o') + 
lema('[Ee]miti_ó__o') + 
lema('[Ee]ncubri_ó__o') + 
lema('[Ee]scindi_ó__o') + 
lema('[Ee]scribi_ó__o') + 
lema('[Ee]sculpi_ó__o') + 
lema('[Ee]scupi_ó__o') + 
lema('[Ee]sgrimi_ó__o') + 
lema('[Ee]vadi_ó__o', pre=['Néstor ']) + 
lema('[Ee]xhibi_ó__o') + 
lema('[Ee]xisti_ó__o') + 
lema('[Ee]xpandi_ó__o') + 
lema('[Ee]xt__endió_i') + 
lema('[Ff]ormar_í_a[ns]?_i') + 
lema('[Ff]_ue__(?:ú[eé]|ué)') + 
lema('[Ff]undi_ó__o') + 
lema('[Hh]i_c_ieron_z') + 
lema('[Hh]ic_i_eron_') + 
lema('[Hh]undi_ó__o') + 
lema('[Ii]mparti_ó__o') + 
lema('[Ii]mprimi_ó__o') + 
lema('[Ii]ncidi_ó__o') + 
lema('[Ii]ncumpli_ó__o') + 
lema('[Ii]ncurri_ó__o') + 
lema('[Ii]nhibi_ó__o') + 
lema('[Ii]nscribi_ó__o') + 
lema('[Ii]nsisti_ó__o') + 
lema('[Ii]nterrumpi_ó__o') + 
lema('[Ii]nvadi_ó__o') + 
lema('[Ii]rrumpi_ó__o') + 
lema('[Mm]u__rieron_e') + 
lema('[Mm]uri_ó__o', pre=['Jordi ']) + #Apellido
lema('[Nn]utri_ó__o') + 
lema('[Oo]curri_ó__o') + 
lema('[Oo]miti_ó__o') + 
lema('[Pp]ari_ó__o') + 
lema('(?<![Cc]orazón )[Pp]arti_ó__o') + 
lema('[Pp]ercibi_ó__o') + 
lema('[Pp]erif_é_ric[ao]s?_e') + 
lema('[Pp]ermiti_ó__o') + 
lema('[Pp]ersisti_ó__o') + 
lema('[Pp]ersuadi_ó__o') + 
lema('[Pp]ervivi_ó__o') + 
lema('[Pp]olic_í_as?_i') + 
lema('[Pp]redefini_ó__o') + 
lema('[Pp]rescindi_ó__o') + 
lema('[Pp]rescribi_ó__o') + 
lema('[Pp]resumi_ó__o') + 
lema('[Pp]rodu_jo__ci[oó]') + 
lema('[Pp]roscribi_ó__o') + 
lema('[Pp]u__dieron_e') + 
lema('[Pp]uli_ó__o') + 
lema('[Rr]a_í_z_i', pre=['na ']) + lema('[Rr]a_í_ces_i') + 
lema('[Rr]e_s_pondió_') + 
lema('[Rr]eabri_ó__o') + 
lema('[Rr]easumi_ó__o') + 
lema('[Rr]ebati_ó__o') + 
lema('[Rr]ecibi_ó__o') + 
lema('[Rr]ecubri_ó__o') + 
lema('[Rr]ecurri_ó__o') + 
lema('[Rr]edefini_ó__o') + 
lema('[Rr]edescubri_ó__o') + 
lema('[Rr]edimi_ó__o') + 
lema('[Rr]edu_j_eron_ci') + 
lema('[Rr]eescribi_ó__o') + 
lema('[Rr]eimprimi_ó__o') + 
lema('[Rr]eincidi_ó__o') + 
lema('[Rr]emiti_ó__o') + 
lema('[Rr]eparti_ó__o') + 
lema('[Rr]epercuti_ó__o') + 
lema('[Rr]eprimi_ó__o') + 
lema('[Rr]escindi_ó__o') + 
lema('[Rr]esidi_ó__o') + 
lema('[Rr]esisti_ó__o') + 
lema('[Rr]esumi_ó__o') + 
lema('[Rr]etransmiti_ó__o') + 
lema('[Rr]evivi_ó__o') + 
lema('[Ss]_i_guieron_e') + 
lema('[Ss]acudi_ó__o') + 
lema('[Ss]o_r_prendió_') + 
lema('[Ss]obrevivi_ó__o') + 
lema('[Ss]ubdividi_ó__o') + 
lema('[Ss]ubi_ó__o') + 
lema('[Ss]ubsisti_ó__o') + 
lema('[Ss]ucumbi_ó__o') + 
lema('[Ss]ufri_ó__o') + 
lema('[Ss]uicid__ó_i') + 
lema('[Ss]upli_ó__o') + 
lema('[Ss]uprimi_ó__o') + 
lema('[Ss]urti_ó__o') + 
lema('[Ss]uscribi_ó__o') + 
lema('[Tt]amb_ié_n_(?:ie|í[eé])') + 
lema('[Tt]endr_a_[ns]?_a') + 
lema('[Tt]endr_í_a[ns]?_i') + 
lema('[Tt]odav_í_a_i') + 
lema('[Tt]ra__slad(?:ad|)[ao]s?_n') + 
lema('[Tt]ranscribi_ó__o') + 
lema('[Tt]ranscurri_ó__o') + 
lema('[Tt]ransmiti_ó__o') + 
lema('[Tt]rascurri_ó__o') + 
lema('[Tt]rasmiti_ó__o') + 
lema('[Uu]rdi_ó__o') + 
lema('[VvLl]_éase t_ambi[eé]n_(?:ea[sc][eé] [Tt]|éace t|eá[sc][eé] [tT])') + lema('[Vv]_éase__(?:eas[eé]|eáse)') + 
lema('vivi_ó__o') + #Subaru Vivio
lema('(?<![Vv]alle de )[Vv]i_o_(?!\]\])_ó') + 
lema('_á_rbol(?!\]\][a-z]+)_a') + lema('_á_rboles_a') + lema('_Á_rbol(?:es|)_A') + 
lema('[Aa]h_í_(?!\'ezer)_i', pre=['di ']) + #546
lema('[Aa]batir_á_[ns]?_a') + 
lema('[Aa]brir_á_[ns]?_a') + 
lema('[Aa]burrir_á_[ns]?_a') + 
lema('[Aa]cudir_á_[ns]?_a') + 
lema('[Aa]dmitir_á_[ns]?_a') + 
lema('[Aa]dscribir_á_[ns]?_a') + 
lema('[Aa]ludir_á_[ns]?_a') + 
lema('[Aa]percibir_á_[ns]?_a') + 
lema('[Aa]plaudir_á_[ns]?_a') + 
lema('[Aa]sistir_á_[ns]?_a') + 
lema('[Aa]sumir_á_[ns]?_a') + 
lema('[Aa]turdir_á_[ns]?_a') + 
lema('[Aa]ñadir_á_[ns]?_a') + 
lema('[Bb]atir_á_[ns]?_a') + 
lema('[Cc]ircunscribir_á_[ns]?_a') + 
lema('[Cc]oescribir_á_[ns]?_a') + 
lema('[Cc]oexistir_á_[ns]?_a') + 
lema('[Cc]oincidir_á_[ns]?_a') + 
lema('[Cc]ombatir_á_[ns]?_a') + 
lema('[Cc]ompartir_á_[ns]?_a') + 
lema('[Cc]oncurrir_á_[ns]?_a') + 
lema('[Cc]onfundir_á_[ns]?_a') + 
lema('[Cc]onsistir_á_[ns]?_a') + 
lema('[Cc]onsumir_á_[ns]?_a') + 
lema('[Cc]onvivir_á_[ns]?_a') + 
lema('[Cc]ubrir_á_[ns]?_a') + 
lema('[Cc]umplir_á_[ns]?_a') + 
lema('[Cc]undir_á_[ns]?_a') + 
lema('[Dd]ebatir_á_[ns]?_a') + 
lema('[Dd]ecidir_á_[ns]?_a') + 
lema('[Dd]efinir_á_[ns]?_a') + 
lema('[Dd]escribir_á_[ns]?_a') + 
lema('[Dd]escubrir_á_[ns]?_a') + 
lema('[Dd]esistir_á_[ns]?_a') + 
lema('[Dd]ifundir_á_[ns]?_a') + 
lema('[Dd]imitir_á_[ns]?_a') + 
lema('[Dd]irimir_á_[ns]?_a') + 
lema('[Dd]iscurrir_á_[ns]?_a') + 
lema('[Dd]iscutir_á_[ns]?_a') + 
lema('[Dd]isuadir_á_[ns]?_a') + 
lema('[Dd]ividir_á_[ns]?_a') + 
lema('[Ee]ludir_á_[ns]?_a') + 
lema('[Ee]mitir_á_[ns]?_a') + 
lema('[Ee]ncubrir_á_[ns]?_a') + 
lema('[Ee]scindir_á_[ns]?_a') + 
lema('[Ee]scribir_á_[ns]?_a') + 
lema('[Ee]sculpir_á_[ns]?_a') + 
lema('[Ee]scupir_á_[ns]?_a') + 
lema('[Ee]sgrimir_á_[ns]?_a') + 
lema('[Ee]vadir_á_[ns]?_a') + 
lema('[Ee]xhibir_á_[ns]?_a') + 
lema('[Ee]ximir_á_[ns]?_a') + 
lema('[Ee]xistir_á_[ns]?_a') + 
lema('[Ee]xpandir_á_[ns]?_a') + 
lema('[Ff]undir_á_[ns]?_a') + 
lema('[Hh]undir_á_[ns]?_a') + 
lema('[Ii]mpartir_á_[ns]?_a') + 
lema('[Ii]mprimir_á_[ns]?_a') + 
lema('[Ii]ncidir_á_[ns]?_a') + 
lema('[Ii]ncumplir_á_[ns]?_a') + 
lema('[Ii]ncurrir_á_[ns]?_a') + 
lema('[Ii]nfundir_á_[ns]?_a') + 
lema('[Ii]nhibir_á_[ns]?_a') + 
lema('[Ii]nscribir_á_[ns]?_a') + 
lema('[Ii]nsistir_á_[ns]?_a') + 
lema('[Ii]nterrumpir_á_[ns]?_a') + 
lema('[Ii]nvadir_á_[ns]?_a') + 
lema('[Ii]rrumpir_á_[ns]?_a') + 
lema('[Nn]utrir_á_[ns]?_a') + 
lema('[Oo]currir_á_[ns]?_a') + 
lema('[Oo]mitir_á_[ns]?_a') + 
lema('[Pp]arir_á_[ns]?_a') + 
lema('(?<!tu )[Pp]artir_á__a') +lema('[Pp]artir_á_[ns]_a') + 
lema('[Pp]ercibir_á_[ns]?_a') + 
lema('[Pp]ermitir_á_[ns]?_a') + 
lema('[Pp]ersistir_á_[ns]?_a') + 
lema('[Pp]ersuadir_á_[ns]?_a') + 
lema('[Pp]ervivir_á_[ns]?_a') + 
lema('[Pp]redefinir_á_[ns]?_a') + 
lema('[Pp]rescindir_á_[ns]?_a') + 
lema('[Pp]rescribir_á_[ns]?_a') + 
lema('[Pp]residir_á_[ns]?_a') + 
lema('[Pp]resumir_á_[ns]?_a') + 
lema('[Pp]roducir_á_[ns]?_a') + 
lema('[Pp]roscribir_á_[ns]?_a') + 
lema('[Pp]ulir_á_[ns]?_a') + 
lema('[Rr]eabrir_á_[ns]?_a') + 
lema('[Rr]easumir_á_[ns]?_a') + 
lema('[Rr]ebatir_á_[ns]?_a') + 
lema('[Rr]ecibir_á_[ns]?_a') + 
lema('[Rr]ecubrir_á_[ns]?_a') + 
lema('[Rr]ecurrir_á_[ns]?_a') + 
lema('[Rr]edefinir_á_[ns]?_a') + 
lema('[Rr]edescubrir_á_[ns]?_a') + 
lema('[Rr]edimir_á_[ns]?_a') + 
lema('[Rr]eescribir_á_[ns]?_a') + 
lema('[Rr]eimprimir_á_[ns]?_a') + 
lema('[Rr]eincidir_á_[ns]?_a') + 
lema('[Rr]emitir_á_[ns]?_a') + 
lema('[Rr]epartir_á_[ns]?_a') + 
lema('[Rr]epercutir_á_[ns]?_a') + 
lema('[Rr]eprimir_á_[ns]?_a') + 
lema('[Rr]escindir_á_[ns]?_a') + 
lema('[Rr]esidir_á_[ns]?_a') + 
lema('[Rr]esistir_á_[ns]?_a') + 
lema('[Rr]esumir_á_[ns]?_a') + 
lema('[Rr]etransmitir_á_[ns]?_a') + 
lema('[Rr]evivir_á_[ns]?_a') + 
lema('[Ss]acudir_á_[ns]?_a') + 
lema('[Ss]obrevivir_á_[ns]?_a') + 
lema('[Ss]ubdividir_á_[ns]?_a') + 
lema('[Ss]ubir_á__a', post=['Sánchez ']) + lema('[Ss]ubir_á_[ns]_a') + 
lema('[Ss]ubsistir_á_[ns]?_a') + 
lema('[Ss]ucumbir_á_[ns]?_a') + 
lema('[Ss]ufrir_á_[ns]?_a') + 
lema('[Ss]umir_á_[ns]?_a') + 
lema('[Ss]uplir_á_[ns]?_a') + 
lema('[Ss]uprimir_á_[ns]?_a') + 
lema('[Ss]urtir_á_[ns]?_a') + 
lema('[Ss]uscribir_á_[ns]?_a') + 
lema('[Tt]ranscribir_á_[ns]?_a') + 
lema('[Tt]ranscurrir_á_[ns]?_a') + 
lema('[Tt]ransmitir_á_[ns]?_a') + 
lema('[Tt]rascurrir_á_[ns]?_a') + 
lema('[Tt]rasmitir_á_[ns]?_a') + 
lema('[Uu]nir_á_[ns]?_a') + 
lema('[Uu]rdir_á_[ns]?_a') + 
lema('[Vv]ivir_á_[ns]?_a') + 
lema('[Mm]ie_m_bros?_n') + 
lema('(?<![Ss]uo )[Dd]isc_í_pulos?_i') + 
lema('[Pp]arec_í_a[ns]?_i') + 
lema('[Ii]ncon_s_cientes?_') + 
lema('[Pp]ercan_c_es?_s') + 
lema('[Aa]bsolvi_ó__o') + 
lema('[Aa]utodisolvi_ó__o') + 
lema('[Cc]ondoli_ó__o') + 
lema('[Cc]onmovi_ó__o') + 
lema('[Dd]emoli_ó__o') + 
lema('[Dd]esenvolvi_ó__o') + 
lema('[Dd]evolvi_ó__o') + 
lema('[Dd]isolvi_ó__o') + 
lema('(?<!Juan )[Dd]oli_ó__o') + 
lema('[Ee]nvolvi_ó__o') + 
lema('[Ll]lovi_ó__o', pre=['Túnel de ']) + 
lema('[Mm]oli_ó__o') + 
lema('[Mm]ordi_ó__o') + 
lema('[Mm]ovi_ó__o', pre=['Gonzalo ']) + 
lema('[Pp]romovi_ó__o') + 
lema('[Rr]emordi_ó__o') + 
lema('[Rr]emovi_ó__o') + 
lema('[Rr]esolvi_ó__o') + 
lema('[Rr]evolvi_ó__o') + 
lema('[Vv]olvi_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abanic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abarranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abdic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aboc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aborrasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abronc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acerc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)achac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)achic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acidific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acurruc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adjudic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahorc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahuec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alambic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alterc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amplific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apalanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aparc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apenc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aplac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atrac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atrinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)autentic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)autentific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)avoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)banc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)beatific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bifurc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)biloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bisec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bonific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)brinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)busc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)caduc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)calc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)calcific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)calific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)capisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)casc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)centuplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cerc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)certific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chamusc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)choc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)churrusc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)clarific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)clasific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)claudic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)codific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)complic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comunic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conculc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contraatac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contraindic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)convoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cosific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)critic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)crucific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuadriplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuadruplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cualific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuantific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cubic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)damnific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decalcific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decodific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decortic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dedic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)defec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)demarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)densific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deprec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)derroc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desacidific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaparc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desatanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desatasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desatranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbarranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desboc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descalcific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descalific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desclasific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descodific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descoloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desconvoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desembarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desemboc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desempac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desenfoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desenrosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desertific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desfalc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desintoxic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmitific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desnuc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despeluc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despotric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)destac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desubic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diagnostic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dignific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diversific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)domestic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dosific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dulcific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)duplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)edific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)educ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ejemplific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)electrific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embarranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embauc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embelec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emboc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emborrasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embroc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embronc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emperic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enamoric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encharc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfrasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enmarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enroc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enrosc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entrechoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entresac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entronc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)equivoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)erradic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escarific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escenific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esparranc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)especific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estanc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estatific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estratific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estuc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)evoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)explic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fabric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)falsific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fornic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fortific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fructific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gasific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)glorific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gratific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hamac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hipotec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hocic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)humidific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)identific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imbric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)implic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imprec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impurific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incomunic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inculc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)indic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intensific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intercomunic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intoxic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intrinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)invoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)justific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lenific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lentific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lignific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lubric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lubrific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)machac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)machuc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)magnific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)maleduc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manduc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)marc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)marisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)masc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)masific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mastic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)medic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)merc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mistific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mitific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mixtific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)modific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)molific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)momific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mortific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)multiplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)music_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)nevisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)nidific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)notific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)obcec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ofusc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)olisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)osific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pacific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)panific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pellizc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)penc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perjudic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)personific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pesc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)petrific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pizc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)planific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plantific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plastific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)platic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pontific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)practic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)predic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prefabric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prevaric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pronostic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prosific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)provoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)public_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)purific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)quintuplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)radic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ramific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rarific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rasc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ratific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rebusc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recalc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recalific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recoloc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rectific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reduplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reedific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reeduc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reembarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)refresc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reivindic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remarc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remolc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repesc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)replic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retruc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reubic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reunific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revindic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revivific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ronc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rubric_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sacarific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sacrific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salpic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)santific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)saponific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sec_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)septuplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sextuplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)signific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)simplific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sindic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sofistic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sofoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solidific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sonsac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suberific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)surc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tabic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tecnific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)testific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tipific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)toc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tonific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trabuc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trafic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trinc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)triplic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trompic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)truc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trunc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ubic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)unific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ventisc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)verific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)versific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vindic_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vitrific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vivific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abandon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abjur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abland_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abofete_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abord_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abort_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aboton_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abrev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)abus_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acamp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acapar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acarre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acaudill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)accident_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aceler_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acept_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aclam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aclar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aclimat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acomod_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acompañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acondicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acongoj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aconsej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acopl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acorral_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acort_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acostumbr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acredit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)activ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acultur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acumul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acun_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acus_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)acuñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adapt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adelant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adentr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adiestr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adivin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adjunt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)administr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)admir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adopt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ador_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adorn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ados_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)adueñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aferr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aficion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afiebr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afili_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afirm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afloj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aflor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)afront_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agarr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agasaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aglutin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agrad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agrand_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agrav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agri_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agrup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aguant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)agusan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahond_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahorr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahues_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ahuyent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ajust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alarde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alarm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alborot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alegr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aliger_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aliment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aline_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)allan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)almacen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aloj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alquil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alter_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)altern_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)alumbr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amaestr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amamant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)am_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amarr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ambicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ambient_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amedrent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amerit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amodorr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amold_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amonest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amonton_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amotin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ampar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amput_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)amuebl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ancl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anex_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anexion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anhel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aniquil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anonad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anticip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)antoj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anunci_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)anul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apadrin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apare_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apart_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apasion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apellid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apiad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apiñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aplan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aplast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apod_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apoder_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apostat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apoy_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aprest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apresur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aprision_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aprovech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aproxim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apunt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)apuñal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arbitr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)archiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)argument_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arras_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrastr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrebat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arregl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrejunt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrellan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrib_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrincon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arrodill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arroj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arroll_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)arruin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)articul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asalt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)as_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ase_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asegur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asemej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asesin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asesor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asever_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asimil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asom_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asombr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aspir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)asust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ataj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)at_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atorment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atragant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atrap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atras_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atrincher_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)atropell_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)audicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)audit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)augur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aument_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ausent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)autodenomin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)autonombr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)autoproclam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)auxili_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aval_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aventaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aventur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)avis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)avist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)aviv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ayud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)azot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)babe_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bail_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)baj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)balance_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)balbuce_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)baraj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)batall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bate_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)blanque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)blasfem_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bloque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)boicote_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bombarde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)borde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)borr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bosquej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)brill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)brind_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)brome_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)bronce_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)brot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)buce_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)burl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cabece_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cable_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)calcul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)call_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)calm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)camin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)camufl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cancel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)canje_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cans_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)capacit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)capitane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)capitul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)capt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)captur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)castr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)catapult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)caus_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cautiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ceb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)celebr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cens_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)censur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)centr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cercen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ces_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chate_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cheque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)chorre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cifr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ciment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)circul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)clam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)clausur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)clav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coadyuv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cobij_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cobr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cocin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cofund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colabor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colaps_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coleccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colision_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)colore_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comand_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)combin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comision_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)compagin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)compar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)compenetr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)compens_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comi_ó__o') + #comio
lema('[Ss]e (?:me |te |l[aeo]s? |)compil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)complement_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)complet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)compr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comprob_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)comput_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)concentr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)concit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)concret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)concurs_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)condecor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conden_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)condicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)condon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confeccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)configur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confirm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confront_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)congel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conjetur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conjur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conllev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conmemor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conmin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conmocion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conmut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conquist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consagr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conserv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consider_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consolid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)conspir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)const_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)constat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)constip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)consum_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contact_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contamin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contempl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)content_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contrarrest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contrast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)contrat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)control_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)convalid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)convers_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cooper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coordin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cop_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coquete_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coron_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)correte_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)corrobor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cort_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cortej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cosech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)coste_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cotej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cronometr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuchiche_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuestion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cuid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)culmin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)culp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cultiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)curr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)curs_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deambul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)debilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)debit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)debut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decapit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decepcion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)declam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)declar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)declin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)decret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)defraud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)degener_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)degrad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)degust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)delat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deleit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)delimit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deline_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)demand_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)demor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)denomin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)denot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)depar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deposit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deriv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)derram_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)derrib_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)derrot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)derrumb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaceler_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaconsej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desacopl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desacredit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desactiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desagrad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desagrup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaloj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desanim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desaprovech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desarm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desar_rolló__r?oll?o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desarticul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desatornill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desayun_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbarat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbloque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desbord_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descans_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descarril_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descart_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descentr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descifr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descojon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desconect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descontrol_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)descuid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desdas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desdeñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desdobl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dese_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desempeñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desencaden_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desenred_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desenvain_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desestim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desfil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desgaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desgarr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deshidrat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)design_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desilusion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desintegr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desinteres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deslind_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deslumbr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmantel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmay_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmont_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desmoron_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desnud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despach_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desparasit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despendol_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desplom_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despoj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despreocup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)despunt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)destac_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)destap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)destin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)destron_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desvel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desvel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)desvincul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)detall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)detect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deterior_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)determin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)deton_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)devast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)devor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diagram_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dibuj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dictamin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dict_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diezm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dificult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dilat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diplom_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)discrep_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)discrimin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disculp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disemin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)diseñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disfrut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disgust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dispar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dispens_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dispers_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)disput_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)distorsion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)divis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dobl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)doctor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)document_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)domin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)don_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)dur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)eclips_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)edit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)efectu_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)egres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ejecut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ejercit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)elabor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)elev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)elimin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)elucid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)eman_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emancip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embalsam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embeles_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)embols_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emborrach_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emigr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emocion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emparej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empecin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empeor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empeñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emple_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empuj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)empuñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)emul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enajen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enamor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enarbol_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encaden_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encamin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encarcel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encariñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encarn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encorv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encuadr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)encumbr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)endeud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)endos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enemist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enferm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enfrent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enganch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)engañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)engendr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)englob_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)engrip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enlist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enoj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enred_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enrol_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ensambl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ensanch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ensay_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enseñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ensimism_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entabl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enter_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enton_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entrañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entrevist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)entusiasm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enumer_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)envenen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)enviud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)equilibr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)equip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)equipar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)erosion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)eruct_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escamp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escaque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escatim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escolt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escuch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)escudriñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esfum_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esmer_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)espant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)especul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)especific_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)espet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)espole_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esput_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)esquiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estacion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estaf_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estamp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estereotip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estimul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estipul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estoque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estorb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estrangul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estrech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estrell_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estrope_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estructur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)estruj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)etiquet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)evapor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)evit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)evolucion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exacerb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exager_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exalt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)examin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)excav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)excit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exclam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)excus_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exhort_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exhum_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)exoner_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)experiment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)expir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)explor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)explot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)export_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)expres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)expuls_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)extermin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)extrañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)eyect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)facilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)factur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)facult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)faj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)falt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fantase_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fascin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)felicit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)festej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)festone_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fich_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)figur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fij_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)film_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)filosof_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)filtr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)firm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)flame_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)flet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)flot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)foment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fonde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)forceje_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)forj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)form_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)formate_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)formul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)forr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fracas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fraccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fractur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fragment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)frecuent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fris_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)frustr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fulmin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)funcion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fundament_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fusil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)fusion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)galardon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gangren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gener_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)germin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gestion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)glori_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)glos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gole_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)golpe_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)grab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gradu_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)granje_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)grit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)guard_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)guerre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)guill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)guis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)guiñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)gust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)habilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)habit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)habl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hart_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hered_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)herman_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hibern_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)homenaje_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)honr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hosped_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)hueve_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)humill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)husme_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ide_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ignor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)igual_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ilumin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ilustr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imagin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impact_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impetr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)implant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)implement_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)implor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)import_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imposibilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impost_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impregn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impresion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)improvis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impugn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)impuls_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)imput_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inaugur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incapacit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incaut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incentiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inclin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incorpor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)increment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)increp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incrust_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incub_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)incursion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)indigest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)indign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)indult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)infect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)infiltr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ingres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inhabilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inmigr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)innov_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inquiet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)insert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)insinu_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inspeccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inspir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)instal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inst_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)instaur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)instrument_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)insult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)integr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intercal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intercept_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)interconect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)interes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intern_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)interpel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)interpret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)intitul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)invalid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)invent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)invit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)involucr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)inyect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)irrit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jact_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jade_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jiñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jubil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)junt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jurament_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)jur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)labor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)labr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lagrime_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lament_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lastim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)legisl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)legitim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lesion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)levant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)levit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lib_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)liber_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)libr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)licit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lider_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lij_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)limit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)liquid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)list_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)llam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)llen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)llev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)llor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)lo_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)logr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)luch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)madur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)malinterpret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)malogr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)maltrat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mand_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)maniobr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manipul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manufactur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)maravill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)march_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)marchit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mare_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)margin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)marin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)martill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)masacr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)masturb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)matricul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)me_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)medit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mejor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mencion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mene_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)merm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mezcl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)migr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)milit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)min_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)model_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)moder_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mof_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)moj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)molde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)molest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mont_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)motiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)murmur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)mutil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)nad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)naj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)narr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)necesit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)nombr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)nomin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)noque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)not_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)numer_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)objet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)obnubil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)obr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)observ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)obsesion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)obstin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ocasion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ocult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ocup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ofert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)oje_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)olvid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)onde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)oper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)opin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)opt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)or_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)orbit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)orden_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ore_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)orient_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)origin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)orquest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)os_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)oscil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ostent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ovacion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pact_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pagin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)parafrase_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)par_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)parpade_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)particip_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pase_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)patale_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pate_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)patent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)patin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)patrocin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)patrull_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)paviment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pedale_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pein_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pele_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)penetr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)percat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perdon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perdur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)peregrin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perfeccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perfil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perfor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)permut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pernoct_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perpetr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perpetu_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)persign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)person_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)perturb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pilot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pinch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pint_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pirar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pirate_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pivot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)planch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plante_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)plasm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pleite_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ponch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)popul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)port_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)posesion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)posibilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)posicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)postul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)precipit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)precis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)predomin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prefij_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pregon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)pregunt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)preocup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prepar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)present_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)preserv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)presion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)priv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)proces_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)procesion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)proclam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)procre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)procur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)profes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)program_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)progres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prolifer_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)promocion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)propin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)proporcion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)propugn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)propuls_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)prosper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)protest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)proyect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)publicit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)public_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)puj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)puls_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)puntu_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)quebrant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)qued_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)quej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)quem_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)querell_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)quit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rapt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rasguñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rastre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ray_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)razon_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reaccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reacondicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reactiv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reafirm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reagrup_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reanim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reanud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rearm_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reasign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reaviv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rebaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reban_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rebas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rebel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rebot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recaptur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recaud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recicl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reclam_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reclut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recobr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recolect_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recombin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recompens_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reconquist_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reconsider_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recopil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recort_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recre_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recrimin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)recuper_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)redact_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)redireccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rediseñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)redobl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)redonde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)redund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reedit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reelabor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reencarn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reentr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reestren_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reestructur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)refin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reflej_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reflexion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reformul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)refrend_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)refund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)refut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regañ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)registr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reglament_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regrab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)regul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rehabilit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rein_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reinaugur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reincorpor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reingres_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reinstal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reinstaur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reintegr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reinterpret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reinvent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reiter_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)relacion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)relaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)relampague_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)relat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)relev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rellen_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remed_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rememor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remezcl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remodel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)remont_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)renombr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)renov_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reorden_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reorient_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repatri_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)replante_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)report_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)repos_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)represent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reproch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reprogram_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)requis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resalt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resbal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rescat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reserv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)reseñ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resguard_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resign_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)respald_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)respet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rest_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)restaur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)resucit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)result_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ret_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retard_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retom_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retorn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retract_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retras_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)retrat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revalid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)revolucion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rob_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rode_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rond_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)rumore_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sabore_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sabote_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sald_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salte_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)salv_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)san_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sancion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sangr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)saque_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)secuestr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)secund_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)seleccion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sell_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)separ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sepult_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sesion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)señal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)silb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)simul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)simultane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)soborn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sobrepas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)socav_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solicit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solucion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)solvent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sonde_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sopes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sopl_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)soport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sorte_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)soslay_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sospech_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subast_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subestim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sublev_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sublim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subordin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subray_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subsan_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)subtitul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sud_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sugestion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suicid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sujet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sum_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suministr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)super_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)supervis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suplant_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)suscit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sustent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)susurr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tach_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tal_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tall_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tarare_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tard_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tartamude_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)telefone_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)teletransport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)televis_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)telone_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)templ_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tergivers_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)termin_ó__o') + lema('(?:[Aa]l|[Dd]el|[Uu]n|[Ss]u|[Ee]l) t_é_rmino_e') + lema('[Ll]os t_é_rminos_e') + lema('[Tt]ermin_ó_ (?:con|en|[0-9]+)_o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)test_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tild_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)titube_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)titul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)toler_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tom_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)top_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tore_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)torn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)torpede_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tortur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trabaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trab_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)traicion_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tram_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tramit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)transform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)transit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)transparent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)transport_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trape_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trasform_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)traslad_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trasnoch_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)traspas_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trastabill_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trastoc_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trastorn_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trat_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)trep_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tribut_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tritur_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)triunf_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tumb_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)tute_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ufanar_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ultim_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)unt_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)us_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)usurp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vacil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)valid_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)valor_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vaticin_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vener_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)verane_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vers_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)version_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vet_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)viaj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vigil_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vincul_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)viol_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)violent_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vir_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vision_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)visit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vislumbr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)volte_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vomit_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vot_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)vulner_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zaf_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zanj_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zap_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zarp_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zozobr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)zurr_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)cerr_ó__o')+ 
lema('[Ss]e (?:me |te |l[aeo]s? |)mel_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)eximi_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)confes_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ment_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)concert_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)manifest_ó__o') + 
lema('[Cc]iudad__es_d') + 
lema('[Aa]cert_ó_(?! dos)_o') + 
lema('[Aa]crecent_ó__o') + 
lema('[Aa]lent_ó__o', post=[', 2011']) + 
lema('[Aa]pacent_ó__o') + 
lema('[Aa]pret_ó__o') + 
lema('[Aa]rrend_ó__o') + 
lema('[Aa]sent_ó__o') + 
lema('[Aa]serr_ó__o') + 
lema('[Aa]test_ó__o') + 
lema('[Aa]traves_ó__o') + 
lema('[Aa]vent_ó__o') + 
lema('[Bb]eld_ó__o') + 
lema('[Cc]alent_ó__o') + 
lema('[Dd]esacert_ó__o') + 
lema('[Dd]esalent_ó__o') + 
lema('[Dd]esaterr_ó__o') + 
lema('[Dd]esconcert_ó__o') + 
lema('[Dd]esenterr_ó__o') + 
lema('[Dd]esgobern_ó__o') + 
lema('[Dd]eshel_ó__o') + 
lema('[Dd]esmembr_ó__o') + 
lema('[Dd]espert_ó__o') + 
lema('[Ee]mparent_ó__o') + 
lema('[Ee]mpedr_ó__o') + 
lema('[Ee]ncerr_ó__o') + 
lema('[Ee]ncomend_ó__o') + 
lema('[Ee]nmel_ó__o') + 
lema('[Ee]nmend_ó__o') + 
lema('[Ee]nsangrent_ó__o') + 
lema('[Ee]nterr_ó__o', pre=['O '], post=[' da']) + 
lema('[Ee]ntrecerr_ó__o') + 
lema('[Ee]scarment_ó__o') + 
lema('[Gg]obern_ó_(?! de Galicia)_o') + 
lema('[Hh]err_ó__o') + 
lema('[Ii]ncens_ó__o', post=[' e discordia']) + 
lema('[Mm]erend_ó__o') + 
lema('Quebr_ó__o', post=['[,\]]']) +lema('quebr_ó__o') + 
lema('[Rr]ecalent_ó__o') + 
lema('[Rr]ecomend_ó__o') + 
lema('[Rr]emend_ó__o') + 
lema('[Rr]epens_ó__o') + 
lema('[Rr]equebr_ó__o') + 
lema('[Rr]event_ó__o') + 
lema('[Ss]alpiment_ó__o') + 
lema('[Ss]embr_ó__o') + 
lema('[Ss]obrecalent_ó__o') + 
lema('[Ss]oterr_ó__o') + 
lema('[Ss]ubarrend_ó__o') + 
lema('[Tt]embl_ó__o') + 
lema('[Tt]ent_ó__o') + 
lema('[Pp]rotag_ó_nic[ao]s?_o') + 
lema('[Dd]ram_á_tic[ao]s?_a') + 
lema('[Aa]dhiri_ó__o') + 
lema('[Aa]dvirti_ó__o') + 
lema('[Aa]rrepinti_ó__o') + 
lema('[Aa]sinti_ó__o') + 
lema('[Cc]ircunfiri_ó__o') + 
lema('[Cc]onfiri_ó__o') + 
lema('[Cc]onsinti_ó__o') + 
lema('[Cc]onvirti_ó__o') + 
lema('[Dd]esminti_ó__o') + 
lema('[Dd]ifiri_ó__o') + 
lema('[Dd]igiri_ó__o') + 
lema('[Dd]isinti_ó__o') + 
lema('[Dd]ivirti_ó__o') + 
lema('[Hh]iri_ó__o') + 
lema('[Hh]irvi_ó__o') + 
lema('[Ii]nfiri_ó__o') + 
lema('[Ii]ngiri_ó__o') + 
lema('[Ii]njiri_ó__o') + 
lema('[Ii]nterfiri_ó__o') + 
lema('[Ii]nvirti_ó__o') + 
lema('[Mm]alhiri_ó__o') + 
lema('[Mm]inti_ó__o') + 
lema('[Pp]ervirti_ó__o') + 
lema('[Pp]refiri_ó__o') + 
lema('[Pp]resinti_ó__o') + 
lema('[Pp]rofiri_ó__o') + 
lema('[Rr]econvirti_ó__o') + 
lema('[Rr]efiri_ó__o') + 
lema('[Rr]einvirti_ó__o') + 
lema('[Rr]equiri_ó__o') + 
lema('[Rr]esinti_ó__o') + 
lema('[Rr]evirti_ó__o') + 
lema('[Ss]inti_ó__o') + 
lema('[Ss]ubvirti_ó__o') + 
lema('[Ss]ugiri_ó__o') + 
lema('[Tt]ransfiri_ó__o') + 
lema('[Tt]rasfiri_ó__o') + 
lema('[Zz]ahiri_ó__o') + 
lema('[Dd]escono_c_id[ao]s?_s') + 
lema('[Ee]stu_v_(?:[eo]|ieron|iese[ns]?|iera[ns]?)_b') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)infundi_ó__o') + #Infundio
lema('[Ss]e (?:me |te |l[aeo]s? |)pens_ó__o') + #Penso
lema('[Ss]e (?:me |te |l[aeo]s? |)sent_ó__o') + #Sento LLobelllema('[Cc]iudad__es_d') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)sumi_ó__o') + #Sumio
lema('[Ss]e (?:me |te |l[aeo]s? |)dent_ó__o') + #dento-gingival
lema('[Aa]ut_on_ómic[ao]s?_') + 
lema('[Bb]oleter_í_as?_i') + 
lema('[Aa]basteci_ó__o') + 
lema('[Aa]borreci_ó__o') + 
lema('[Aa]caeci_ó__o') + 
lema('[Aa]conteci_ó__o') + 
lema('[Aa]creci_ó__o') + 
lema('[Aa]doleci_ó__o') + 
lema('[Aa]dormeci_ó__o') + 
lema('[Aa]gradeci_ó__o') + 
lema('[Aa]maneci_ó__o') + 
lema('[Aa]nocheci_ó__o') + 
lema('[Aa]pareci_ó__o') + 
lema('[Aa]peteci_ó__o') + 
lema('[Aa]tardeci_ó__o') + 
lema('[Aa]utoabasteci_ó__o') + 
lema('[Bb]lanqueci_ó__o') + 
lema('[Cc]areci_ó__o') + 
lema('[Cc]ompadeci_ó__o') + 
lema('[Cc]ompareci_ó__o') + 
lema('[Cc]onoci_ó__o') + 
lema('[Cc]onvaleci_ó__o') + 
lema('[Cc]reci_ó__o') + 
lema('[Dd]ecreci_ó__o') + 
lema('[Dd]esabasteci_ó__o') + 
lema('[Dd]esagradeci_ó__o') + 
lema('[Dd]esapareci_ó__o') + 
lema('[Dd]esconoci_ó__o') + 
lema('[Dd]esentumeci_ó__o') + 
lema('[Dd]esfalleci_ó__o') + 
lema('[Dd]esfavoreci_ó__o') + 
lema('[Dd]esguarneci_ó__o') + 
lema('[Dd]esmereci_ó__o') + 
lema('[Dd]esobedeci_ó__o') + 
lema('[Dd]esvaneci_ó__o') + 
lema('[Ee]mbasteci_ó__o') + 
lema('[Ee]mbebeci_ó__o') + 
lema('[Ee]mbelleci_ó__o') + 
lema('[Ee]mbraveci_ó__o') + 
lema('[Ee]mbruteci_ó__o') + 
lema('[Ee]mpalideci_ó__o') + 
lema('[Ee]mpequeñeci_ó__o') + 
lema('[Ee]mplasteci_ó__o') + 
lema('[Ee]mpobreci_ó__o') + 
lema('[Ee]nalteci_ó__o') + 
lema('[Ee]nardeci_ó__o') + 
lema('[Ee]ncalleci_ó__o') + 
lema('[Ee]ncaneci_ó__o') + 
lema('[Ee]ncareci_ó__o') + 
lema('[Ee]ncegueci_ó__o') + 
lema('[Ee]ndureci_ó__o') + 
lema('[Ee]nflaqueci_ó__o') + 
lema('[Ee]nfureci_ó__o') + 
lema('[Ee]ngrandeci_ó__o') + 
lema('[Ee]nloqueci_ó__o') + 
lema('[Ee]nmoheci_ó__o') + 
lema('[Ee]nmudeci_ó__o') + 
lema('[Ee]nnegreci_ó__o') + 
lema('[Ee]nnobleci_ó__o') + 
lema('[Ee]norgulleci_ó__o') + 
lema('[Ee]nrareci_ó__o') + 
lema('[Ee]nriqueci_ó__o') + 
lema('[Ee]nrojeci_ó__o') + 
lema('[Ee]nronqueci_ó__o') + 
lema('[Ee]nsoberbeci_ó__o') + 
lema('[Ee]nsombreci_ó__o') + 
lema('[Ee]nsordeci_ó__o') + 
lema('[Ee]ntalleci_ó__o') + 
lema('[Ee]nterneci_ó__o') + 
lema('[Ee]ntonteci_ó__o') + 
lema('[Ee]ntorpeci_ó__o') + 
lema('[Ee]ntristeci_ó__o') + 
lema('[Ee]ntumeci_ó__o') + 
lema('[Ee]nvaneci_ó__o') + 
lema('[Ee]nvejeci_ó__o') + 
lema('[Ee]nvileci_ó__o') + 
lema('[Ee]scarneci_ó__o') + 
lema('[Ee]sclareci_ó__o') + 
lema('[Ee]stableci_ó__o') + 
lema('[Ee]stremeci_ó__o') + 
lema('[Ff]alleci_ó__o') + 
lema('[Ff]avoreci_ó__o') + 
lema('[Ff]eneci_ó__o') + 
lema('[Ff]loreci_ó__o') + 
lema('[Ff]ortaleci_ó__o') + 
lema('[Ff]osforeci_ó__o') + 
lema('[Ff]osforesci_ó__o') + 
lema('[Gg]uareci_ó__o') + 
lema('[Gg]uarneci_ó__o') + 
lema('[Hh]umedeci_ó__o') + 
lema('[Ll]anguideci_ó__o') + 
lema('[Mm]ereci_ó__o') + 
lema('[Nn]aci_ó__o') + 
lema('[Oo]bedeci_ó__o') + 
lema('[Oo]bscureci_ó__o') + 
lema('[Oo]freci_ó__o') + 
lema('[Oo]scureci_ó__o') + 
lema('[Pp]adeci_ó__o') + 
lema('[Pp]alideci_ó__o') + 
lema('[Pp]areci_ó__o') + 
lema('[Pp]ereci_ó__o') + 
lema('[Pp]ermaneci_ó__o') + 
lema('[Pp]erteneci_ó__o') + 
lema('[Pp]revaleci_ó__o') + 
lema('[Rr]eapareci_ó__o') + 
lema('[Rr]eblandeci_ó__o') + 
lema('[Rr]econoci_ó__o') + 
lema('[Rr]ecrudeci_ó__o') + 
lema('[Rr]eestableci_ó__o') + 
lema('[Rr]ejuveneci_ó__o') + 
lema('[Rr]enaci_ó__o') + 
lema('[Rr]esplandeci_ó__o') + 
lema('[Rr]estableci_ó__o') + 
lema('[Rr]everdeci_ó__o') + 
lema('[Rr]obusteci_ó__o') + 
lema('[Vv]erdeci_ó__o') + 
lema('[Ss]e (?:me |te |l[aeo]s? |)ciment_ó__o') + #Cimento it,pt
lema('[Ss]e (?:me |te |l[aeo]s? |)hel_ó__o') + #helo aquí
lema('[Aa]p_ó_stol_o', pre=['Tom M\. ', 'Tom M\., ', 'aparece en \('], post=[' (?:Tom M\.|Muzac)', ', Tom M\.']) + lema('[Aa]p_ó_stoles_o') + 
lema('[Aa]post_ó_lico(?! (?:[Mm]uneri|Seggio))_o') + 
lema('(?:[Pp]|[Cc]op)rop__iedad(?:es|)_r') + 
lema('(?:[Cc]on|[Ss](?:ub|))igu_i_entes?_') + 
lema('[Aa]bat(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]br(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]burr(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]cud(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]dmit(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]dscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]lud(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]percib(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]plaud(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]sist(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]sum(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]turd(?:ir|)_í_a[ns]?_i') + 
lema('[Aa]ñad(?:ir|)_í_a[ns]?_i') + 
lema('[Bb]at(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]ircunscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]oescrib(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]oexist(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]oincid(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]ombat(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]ompart(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]oncurr(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]onfund(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]onsist(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]onsum(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]onviv_í_a_i', post=[' [Ll]iteraria']) + lema('[Cc]onviv_í_a[ns]_i') + lema('[Cc]onvivir_í_a[ns]?_i') + 
lema('[Cc]ubr(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]umpl(?:ir|)_í_a[ns]?_i') + 
lema('[Cc]und(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]ebat(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]ecid(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]efin(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]escrib(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]escubr(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]esist(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]ifund(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]imit(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]irim(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]iscurr(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]iscut(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]isuad(?:ir|)_í_a[ns]?_i') + 
lema('[Dd]ivid(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]lud(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]mit(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]ncubr(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]scind(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]scrib(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]sculp(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]scup(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]sgrim(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]vad(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]xhib(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]ximir_í_a[ns]?_i') + lema('[Ee]xim_í_an_i') + #eximia
lema('[Ee]xist(?:ir|)_í_a[ns]?_i') + 
lema('[Ee]xpand(?:ir|)_í_a[ns]?_i') + 
lema('[Ff]und(?:ir|)_í_a[ns]?_i') + 
lema('[Hh]und(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]mpart(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]mprim(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]ncid(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]ncumpl(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]ncurr(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nfund(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nhib(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nsist(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nterrump(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]nvad(?:ir|)_í_a[ns]?_i') + 
lema('[Ii]rrump(?:ir|)_í_a[ns]?_i') + 
lema('[Nn]utr(?:ir|)_í_an_i') + #nutrias
lema('[Oo]curr(?:ir|)_í_a[ns]?_i') + 
lema('[Oo]mit(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]arir_í_a[ns]?_i') + #parias
lema('part(?:ir|)_í_a[ns]?_i') + lema('Partir_í_a[ns]?_i') + #Partian
lema('[Pp]ercib(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]ermit(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]ersist(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]ersuad(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]erviv(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]redefin(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]rescind(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]rescrib(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]resid(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]resum(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]roduc(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]roscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Pp]ul(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eabr(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]easum(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]ebat(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]ecib(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]ecubr(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]ecurr(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]edefin(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]edescubr(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]edim(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eescrib(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eimprim(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eincid(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]emit(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]epart(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]epercut(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eprim(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]escind(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]esid(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]esist(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]esum(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]etransmit(?:ir|)_í_a[ns]?_i') + 
lema('[Rr]eviv(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]acud(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]obreviv(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]ubdivid(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]ubir_í_a[ns]?_i') + lema('[Ss]ub_í_an_i') + 
lema('[Ss]ubsist(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]ucumb(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]ufr(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]um(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]upl(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]uprim(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]urt(?:ir|)_í_a[ns]?_i') + 
lema('[Ss]uscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Tt]ranscrib(?:ir|)_í_a[ns]?_i') + 
lema('[Tt]ranscurr(?:ir|)_í_a[ns]?_i') + 
lema('[Tt]ransmit(?:ir|)_í_a[ns]?_i') + 
lema('[Tt]rascurr(?:ir|)_í_a[ns]?_i') + 
lema('[Tt]rasmit(?:ir|)_í_a[ns]?_i') + 
lema('[Uu]nir_í_a[ns]?_i') + lema('[Uu]n_í_a[ns]_i') + lema('[Uu]n_í_a_i', pre=['Miguel ', 'padre '], post=['(?:\]\]|\.es)', ' (?:Tarnów|Demokratyczna|Wolnośći)']) + 
lema('[Uu]rd(?:ir|)_í_a[ns]?_i') + 
lema('viv(?:ir|)_í_a[ns]?_i') + lema('Viv_í_as?_i', pre=['martyre de ']) + lema('Vivir_í_as?_i') + #Vivian
lema('[Aa]comed_í_a[ns]?_i') + 
lema('[Cc]ompet_í_a[ns]?_i') + 
lema('[Cc]onceb_í_a[ns]?_i') + 
lema('[Dd]erret_í_a[ns]?_i') + 
lema('[Dd]esmed_í_a[ns]?_i') + 
lema('[Dd]esped_í_a[ns]?_i') + 
lema('[Dd]esvest_í_a[ns]?_i') + 
lema('[Ee]mbest_í_a[ns]?_i') + 
lema('[Ee]xped_í_a[ns]_i') + #expedia
lema('[Gg]em_í_a[ns]?_i') + 
lema('[Hh]ench_í_a[ns]?_i') + 
lema('[Ii]mped_í_a[ns]?_i') + 
lema('[Ii]nvest_í_a[ns]_i') + #investia
lema('(?<![0-9])[Pp]ed_í_a[ns]?_i') + 
lema('[Pp]reconceb_í_a[ns]?_i') + 
lema('[Rr]end_í_a[ns]?_i') + 
lema('[Rr]epet_í_a[ns]?_i') + 
lema('[Rr]evest_í_a[ns]?_i') + 
lema('(?<!Katepanikion )[Ss]erv_í_as_i') + lema('serv_í_a_i') + lema('[Ss]erv_í_an_i', pre=['Cristian ', 'hermanos ', 'de ', 'Guillermo '], post=['\]\]']) + 
#Servia en
lema('[Tt]ravest_í_a[ns]?_i') + 
lema('[Vv]est_í_a[ns]?_i') + 
lema('[Ii]n_c_identes?_s') + 
lema('[Pp]odr?_í_a[ns]?_i') + 
lema('[Hh]ab_í_a(?! (?:rubica|fuscicauda))_i') + lema('[Hh]abr_í_as_i') + lema('[Hh]abr_í_an_i', pre=['Ain ']) + 
lema('[Aa]van_z_(?:ando|ad[ao]s?|[aoó])_s') + 
lema('(?:[Ss]emi|[Ss]ub|[Hh]iper|[Dd])esa_rroll_(?:ó|os?|a[nrs]?|ad[ao]s?|ando|ador|adora|adores|arse|aron|ar[ií]a[ns]?|aba[ns]?)_(?:roll|rrol)') + lema('[Ss]e (?:me |te |l[aeo]s? |)desarroll_ó__o') +lema('(?:[Ss]emi|[Ss]ub|[Hh]iper|[Dd])esarrollar_í_a[ns]?_i') + 
lema('(?:[Aa]l|[Ee]l|[Ll]as?|[Ll]os|[Mm]is?|[Ss]us?|[Dd]el?|[Pp]ara) ni_ñ_[ao]s?_n') + 
lema('[Aa]tr_á_s_a') + 
lema('[Dd]etr_á_s_a') + 
lema('[Mm]_ás allá__(?:as all[aá]|ás alla)') + lema('[Aa]ll_á_ por_a') + lema('(?:[Ee]stando|[Ee]speraba|[Ll]egaron) all_á__a') + 
lema('(?:[Aa]l|[Dd]el|[Ee]l|[Ee]n|[Ll]os|[Uu]n|[Dd]os|[Tt]res|[Cc]uatro|[Ss]us?|[0-9]+) _á_lbum(?:es|)_a') + lema('(?:[Ee]l|[Ee]n|[Ll]os|[Uu]n|[Dd]os|[Tt]res|[Cc]uatro) _Á_lbum(?:es|)_A') + lema('[Áá]lbum_e_s_(?:ne|)') + lema('_álbu_m(?:es|)_albú') + lema('_Álbu_m(?:es|)_Albú') + 
lema('[Aa]lg_ú_n_u') + #533
#lema('[Aa]ll_á__a') + #2447
lema('[Aa]pocal_i_psis_í') + #567
lema('[Aa]qu_í__i') + #619
#lema('[Aa]_rbóre_(?:as|os?)_rbore') + #803 Arborea Puras matas
lema('[Aa]s_í__i', post=[' (?:dizen|Gonia)']) + #4983
lema('[Aa]uton_ó_mic[ao]s?_o') + #3165
lema('[Bb]ater_í_as?_i') + #699
lema('[Cc]ap_í_tulos?_i') + #535
lema('[Cc]ategor_í_as?(?! del Championat)_i') + #1038
lema('[Cc]r_é_ditos?_e', post=[' in']) + #513
#lema('(?:[Ll]as?|[Uu]nas?|[Cc]ada|[Ss]us?|[Dd]os) [Cc]_ámara_s?_amara') + #544
#lema('(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) [Cc]_ómic_(?![- ](?:Con|[Ss]ans))_omic') + #2527
lema('[Aa]fil_i_ad[ao]s? a_') + 
lema('[Cc]onstru_i_d[ao]s?_í') + #337#89#58
lema('[Dd]em_á_s_a') + #682
lema('[Dd]_é_cadas?_e', post=[' da']) + #602
lema('_ha_ (?:actuado|adaptado|afirmado|agotado|alcanzado|amado|anotado|anunciado|aparecido|arrojado|at(?:ar|ra)vesado|atribuido|aumentado|buscado|calificado|cambiado|caracterizado|casado|causado|cerrado|cobrado|colaborado|comentado|comenzado|competido|comprobado|confirmado|conseguido|conservado|considerado|contado|contestado|continuado|convertido|creado|dado|declarado|dedicado|dejado|demostrado|denominado|desaparecido|desarrollado|desempeñado|desmentido|destacado|disputado|editado|empezado|enamorado|encontrado|enviado|especializado|especulado|estudiado|evolucionado|experimentado|formado|generado|grabado|hecho|identificado|incrementado|indicado|iniciado|inspirado|intentado|interpretado|investigado|jugado|lanzado|llamado|llegado|llenado|llevado|logrado|marcado|mejorado|mencionado|modelado|mostrado|multiplicado|observado|ocupado|participado|pasado|perdido|podido|presentado|provocado|publicado|quedado|realizado|recibido|recuperado|registrado|replanteado|representado|revelado|sacado|señalado|sido|tenido|terminado|tocado|tomado|trabajado|transformado|tratado|usado|utilizado|variado|vendido|venido|visto|vivido|vuelto)_ah?') + lema('__a sus?_h') + # a gabado vacuno| a estado sólido, |puesto|decubierto
lema('[Ee]st_á_ (?!cuando)[a-z]+(?:[ae]ndo|[aáeé]ndose(?:las?|les?|los?|))_a') + lema('[Ee]st_á_ (?:viv[ao]|arriba|abajo|debajo|encima|dad[ao])_a') + lema('(?<![Dd]e )est_á_ muert[ao]_a') + lema('(?<![Aa] )est_á_ bajo_a') + lema('(?<![Ee]stando )est_á_ detrás_a') + lema('[Ee]st_á_n_a') + lema('[Ss]_e_ están?_é') + lema('[Ee]stán? _acostumbrando__aconstumbrando') + lema('[Ee]stán? _adentrando__adrentrando') + lema('[Ee]stán? _alejando__lejando') + lema('[Ee]stán? _asechando__hasechando') + lema('[Ee]stán? _columpiando__colunpeando') + lema('[Ee]stán? _contraatacando__contratacando') + lema('[Ee]stán? _empezando__empesando') + lema('[Ee]stán? _esperando__esparando') + lema('[Ee]stán? _evaluando__valutando de') + lema('[Ee]stán? _fingiendo__fingiando') + lema('[Ee]stán? _preparando__prparando') + lema('[Ee]stán? _vigilando__vijilando') + lema('[Ee]stán? _volviendo viable__viabilizando') + lema('_é_l (?:está|estará|estuvo|es|era|será|fue|tiene|tuvo|tendrá|viene|vendrá|ha|había|se)_e') + lema('_É_l (?:está|estará|estuvo|es|era|será|fue|tiene|tuvo|tendrá|viene|vendrá|ha|había|se)_E') + lema('(?:[Éé]l|[Ee]lla)(?: no|) est_á__a', pre=['a ']) + #1962
lema('[Ee]st_á_ (?:(?:abasteci|aboca|abraza|abriga|absorbi|aburri|acelera|acepta|achata|acompaña|acondiciona|acopla|acorrala|acota|acredita|activa|actualiza|actua|acusa|adapta|adheri|administra|admiti|adorna|adosa|afecta|afilia|afina|agota|agradeci|agrega|agrupa|agujerea|ahueca|ajusta|alfabetiza|alia|alimenta|alinea|almacena|aloja|altera|alumbra|amarra|ambienta|amenaza|ameniza|ampara|amuralla|ancla|anega|apaga|apoya|aproba|armoniza|arrasa|arregla|arrepenti|articula|asegura|asenta|asfalta|asigna|asocia|asusta|atavia|ata|aterra|aterroriza|atesta|atestigua|atrapa|atravesa|atribui|autoriza|avala|basa|basa|baña|bifurca|bloquea|borda|bordea|busca|cablea|calcula|calibra|califica|cambia|canaliza|cansa|canta|capacita|caracteriza|carga|casa|castiga|cataloga|cataloga|categoriza|causa|centraliza|centra|cerca|cerra|certifica|circunda|circunvala|clasifica|clava|codicia|comparti|comprendi|comunica|concesiona|conecta|conforma|considera|constitui|construi|controla|convenci|convoca|correlaciona|corta|crea|data|da|decidi|declara|declar|decora|dedica|defini|defini|delimita|desarrolla|despeja|destina|determina|determina|dirigi|diseña|diseña|distribui|dividi|documenta|domina|domina|dota|embaraza|enamora|encarga|encerra|enfoca|enlaza|equipa|escondi|estableci|estructura|exhibi|fecha|financia|forma|forma|fusiona|goberna|graba|guarda|habita|hendi|hermana|inclui|indefini|indica|influencia|inspira|inspira|integra|interesa|involucra|liga|limita|localiza|obsesiona|ordena|orienta|permiti|posiciona|prepara|programa|prohibi|protagoniza|protegi|realiza|reconoci|rediseña|rega|registra|reglamenta|regula|relaciona|reparti|representa|reserva|restringi|restringi|rodea|rotula|senta|separa|sincroniza|situa|someti|someti|subdividi|subdividi|toma|ubica|uni|vincula)d[ao]|abandonado|agitado|aislado|alejado|animado|aparcado|aprobado|armado|arraigado|asignado|atormentado|atravesado|aumentado|avergonzado|cedido|ceñido|codificado|coronada (?:por|con)|coronado|llamado|marcado|ocupada (?:en|desde|por|y)|ocupado|organizada (?:sobre|por|para|y)|organizado|parado|preocupada (?:a|de|por|porque|con|de)|preocupado|reconocido|retirado)_a') + 
lema('(?:[Ee]l|[Ll]a|[Uu]na?|[Ee]s|[Ff]u[ée]) l_í_der_i') + lema('[Ll]_í_deres_i') + #1465
lema('[Pp]el_í_culas?(?!\.info)_i') + #1320
#lema('_ásper_(?:as|os?)_asper') + lema('_Ásper_(?:as|os?)_Asper') + #530
#lema('_áure_[ao]s?_aure') + lema('_Áure_[ao]s?_Aure') + #1018 Matas
lema('acessado em [0-9]+ de _enero__[Jj]aneiro') + #34
lema('acessado em [0-9]+ de _febrero__[Ff]evereiro') + #34
lema('acessado em [0-9]+ de _marzo__[Mm]arço') + #34
lema('acessado em [0-9]+ de _mayo__[Mm]aio') + #34
lema('acessado em [0-9]+ de _junio__[Jj]uin') + #34
lema('acessado em [0-9]+ de _julio__[Jj]ulho') + #34
lema('acessado em [0-9]+ de _septiembre__[Ss]etembro') + #34
lema('acessado em [0-9]+ de _octubre__[Oo]utubro') + #34
lema('acessado em [0-9]+ de _noviembre__[Nn]ovembro') + #34
lema('acessado em [0-9]+ de _diciembre__[Dd]ezembro') + #34
lema('_consultado el__acessado em') + #34
lema('_consultado__acessado') + #34
#lema('[Dd]_i_putado_e') + #76 cuidado pt
#lema('[Oo]limp_i_adas_í') + #107 olimpiada/olimpíada
#lema('[Aa]pro_b_ad[ao]s?_v') + #30 cuidado pt
lema('[Cc]ent_í_grados?_i') + #32
lema('[Cc]o_o_rdenad[ao]s?_') + #37
lema('[Cc]on_s_iderad[ao]s?_c') + #28
lema('[Cc]ua_d_rad[ao]s?_') + #50
lema('[Cc]ua_n_do se_') + #95
#lema('[Dd]e_s_velad[ao]s?_') + #70 develar/desvelar
lema('[Dd]es_ig_nad[ao]s?_gi') + #86
#lema('[Ee]_x_planada_s') + #37 cuidado pt
lema('[Ee]nv_i_ad[ao]s?_í') + #27
lema('[Ff]rust_r_ad[ao]s?_') + #47
lema('[Hh]_í_gados?_i') + #39
lema('[Ii]nte__grad[ao]s?_n') + #104
lema('[Ii]nte_r_pretad[ao]s?_') + #49
lema('[Mm]edi__ados_d') + #147
lema('[Pp]_u_blicad[ao]s?_ú') + #62
lema('[Ss]_á_bados?_a') + #207
lema('[Mm]i_é_rcoles_e') + 
lema('[Ss]elec_c_ionad[ao]s?_') + #43
lema('[Tt]_i_tulad[ao]s?_í') + #119
lema('[Tt]ra__splantad[ao]s?_n') + #36
lema('[Uu]t_i_lizad[ao]s?_') + #31



#lema('[EE]st_á__a') + 
[]][0]

### 'television' : "lema('[Tt]elevisi_ó_n_o_x')"#Amb. inglés
### 'convivio' : "lema('[Cc]onvivi_ó__o_x')", #Amb. convivio
### 'presidio' : "lema('[Pp]residi_ó__o_x')",# Presidio
### 'invasion' : "lema('[Ii]nvasi_ó_n_o_x')",#Amb. Inglés
### 'sumio' : "lema('[Ss]umi_ó__o_x')", #Nombre
### 'eximio' : "lema('[Ee]ximi_ó__o_x')",#eximio
### 'confeso': "lema('[Cc]onfes_ó__o_x')", #confeso
### 'inverno': "lema('[Ii]nvern_ó__o_x')",#inviernovs invernó
### 'nevo': "lema('[Nn]ev_ó__o_x')", #nuevo/nevó
### 'mento': "lema('[Mm]ent_ó__o_x')", #mentó/mento
### 'concerto': "lema('[Cc]oncert_ó__o_x')", #concierto/concertó/concerto (it)
### 'manifesto': "lema('[Mm]anifest_ó__o_x')",#manifiesto/manifestó
###lema('[Ii]nfundi_ó__o_x') + #Infundio
###lema('[Pp]ens_ó__o_x') + #Penso
###lema('[Ss]ent_ó__o_x') + #Sento LLobell
###lema('[Ss]e (?:me |te |les? |)dent_ó__o_x') + #dento-gingival
###lema('[Ee]sta_b_a[ns]?_v_x') + #portugués
###lema('[Cc]iment_ó__o_x') +
###lema('[Hh]el_ó__o_x') +
###lema('[Pp]aci_ó__o_x') + 
###lema('[Ee]_n_ el [0-9]+_l_x') + lema('[Ee]__l_l e_x') +
###lema('[Mm]ed_í_an_i_x') + #medias, median
###lema('(?<![Ll][\'’])_ú_ltimos?_u_x') + lema('(?<![Ll][\'’])_Ú_ltimos?_U_x') +#Excepciones de por los? un unos el a al del estos? sus? queda[nsr]? quedó y como
#(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) 
#(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) 
#(?:[Aa]l?|[Dd]el?|[Pp]ara|[Ee][nl]|[Hh]acia) 


def compilar():
  flags = re.UNICODE
  pat = ''
  for i in range(len(lemas)):
    p=lemas[i][0]
    pat = pat + '|' + p
    lemas[i][0]=re.compile('\\b('+p+')\\b',flags)
  pat = '\\b('+pat[1:]+')\\b'
  trans = '(.*?)\\b(.{0,40})'+pat+'(.{0,40})\\b(.*?)'
  val = '...\\2\'\'\'\\3\'\'\'\\4...'
  #print (pat)
  return (re.compile(pat,flags),re.compile(trans,flags),val)

linea=''
contenido=''
titulo=''
def proxArticulo(noElimDup, elimExcl, elimRev, excluidos, revisados):
    if len(linea)==0:
        linea = sys.stdin.readline()
    if linea:
        partes = linea.split("]]→",1)
        if len(partes)>1:
            titulo = partes[0].lstrip("[[")
            contenido = partes[1]
            linea = sys.stdin.readline()
            partes = linea.split("]]→",1)
            while titulo == partes[0]:
                contenido += partes[1]
                linea = sys.stdin.readline()
                partes = linea.split("]]→",1)
 

def filtrar(noElimDup, elimExcl, elimRev, excluidos, revisados):
  pat,trans,val = compilar()
  titulo=''
  tituloAnt=''
  contador = 0
  encontrados = 0
  cada = 83660126/1024 #número de líneas 82284502
  contador = 0
  while True:
    linea = sys.stdin.readline()
    if linea:
      contador +=1
      if contador>cada:
        contador = 0
        cada = cada*2
        sys.stderr.write(str(encontrados)+'+')
        encontrados = 0
        sys.stderr.flush()
      partes = linea.split("]]→",1)
      if len(partes)>1:
        titulo = partes[0]
        if titulo!=tituloAnt:
            tituloAnt = titulo;
            #print (titulo)
        #if nuevoTitulo == 'Arte culinario':
        #  print ("****"+linea)
        contenido = url.sub('<url>', partes[1])
        match = pat.search(contenido)
        if match:
          match = trans.match(contenido)
          pal = match.group(3)
          contenido = match.expand(val)
          #print("pal="+pal+" contenido="+contenido)
          print (pal+';'+titulo+']]→'+contenido)
          sys.stdout.flush()
          encontrados +=1
          #contador de las reglas
          for l in lemas:
             if l[0].search(contenido):
                 l[2] += 1
    else:
      sys.stderr.write(str(encontrados)+"\n")
      for l in lemas:
          sys.stdout.write(l[1]+"#"+str(l[2])+"\n")
      break

def main (argv):
   elimDup = True
   elimExcl = True
   elimRev = True
   try:
      opts, args = getopt.getopt(argv,"der",['duplicados', 'excluidos', 'revisados'])
   except getopt.GetoptError:
     #print ("Error")
     print (sys.argv[0]+' [-t] < <inputfile> > <outputfile>')
     print (sys.argv[0]+' [-dh]')
     sys.exit(2)
   for opt, arg in opts:
     if opt in ('-d', '--duplicados'):
       elimDup = False
     elif opt in ('-e', '--excluidos'):
       elimExcl = False
     elif opt in ('-r', '--revisados'):
       elimRev = False
   filtrar(not elimDup, elimExcl, elimRev, excluidos.excluidos, excluidos.revisados)



if __name__ == "__main__":
   main(sys.argv[1:])
