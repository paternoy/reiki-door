import logging

class SequenceMatcher(object):
  def __init__(self):
    self.sequence=[]
    self.targetSequence=[]
    self.sequenceStart=0

  def setTargetSequence(self,target):
    self.targetSequence=SequenceMatcher.normalize(target)

  def addPulse(self,start,duration):
    if not self.sequence:
      self.sequenceStart = start
    self.sequence.append([start-self.sequenceStart,duration])
    logging.debug(self.sequence)

  def cleanup(self):
    self.sequence=[]

  def checkMatch(self):
    if not len(self.sequence)==len(self.targetSequence):
      return False
    normalizedSequence = SequenceMatcher.normalize(self.sequence)
    relativeError=[]
    for i,x in enumerate(self.targetSequence):
      if i==0:
        error=0
      else:
        error = abs(normalizedSequence[i]-x)/x
      relativeError.append(error)
    logging.debug(relativeError)
    return all(item <0.05 for item in relativeError)

  @staticmethod
  def normalize(sequence):
    result=[]
    lastPulseStart = sequence[-1][0]
    for pulse in sequence:
      result.append(pulse[0]/lastPulseStart)
    return result
