class ReedSolomon:
	# INITIALISATION CONSTRUCTOR	
	def __init__(self):
		self.__GFEXP = [0] * 512
		self.__GFLOG = [0] * 256
		self._initialize_fields()

	def _initialize_fields(self):
		self.__GFEXP[0] = 1
		byteValu = 1
		for bytePos in range(1,255):
			byteValu <<= 1
			if (byteValu & 0x100):
				byteValu ^= 0x11d
			self.__GFEXP[bytePos] = byteValu
			self.__GFLOG[byteValu] = bytePos
		for bytePos in range(255,512):
			self.__GFEXP[bytePos] = self.__GFEXP[bytePos - 255]
	
	def __gfMult(self, argX, argY):
		if argX == 0 or argY == 0:
			return 0
		return self.__GFEXP[(self.__GFLOG[argX] + self.__GFLOG[argY]) % 255]
	
	# Galois division
	# argX, argY: dividend, divisor
	# byteValu: quotient
	def __gfDivi(self, argX, argY):
		if argY == 0:
			raise ZeroDivisionError()
		if argX == 0:
			return 0
		return self.__GFEXP[(self.__GFLOG[argX] - self.__GFLOG[argY] + 255) % 255]
	
	## GALOIS POLYNOMIAL OPERATIONS
	# -----
	# Polynomial addition
	# polyA, polyB: polynomial addends
	# polySum: polynomial sum
	def _gfPolyAdd(self, polyA, polyB):
		# initialise the polynomial sum
		polySum = [0] * max(len(polyA), len(polyB))
		
		# process the first addend
		for polyPos in range(0, len(polyA)):
			polySum[polyPos + len(polySum) - len(polyA)] = polyA[polyPos]
		
		# add the second addend
		for polyPos in range(0, len(polyB)):
			polySum[polyPos + len(polySum) - len(polyB)] ^= polyB[polyPos]
		return (polySum)
		
	# Polynomial multiplication
	# polyA, polyB: polynomial factors
	# polyProd: polynomial product
	def _gfPolyMult(self, polyA, polyB):
		# initialise the product
		polyProd = len(polyA) + len(polyB) - 1
		polyProd = [0] * polyProd
		
		for posB in range(0, len(polyB)):
			for posA in range(0, len(polyA)):
				polyProd[posA + posB] ^= self.__gfMult(polyA[posA], polyB[posB])
		return (polyProd)
	
	# Polynomial scaling
	# argPoly: polynomial argument
	# argX: scaling factor
	# polyVal: scaled polynomial
	def _gfPolyScale(self, argPoly, argX):
		# initialise the scaled polynomial
		polyVal = [0] * len(argPoly)
		
		# start scaling
		for polyPos in range(0, len(argPoly)):
			polyVal[polyPos] = self.__gfMult(argPoly[polyPos], argX)
		
		# return the scaled polynomial
		return (polyVal)

	# Polynomial evaluation
	# argPoly: polynomial argument
	# argX: independent variable
	# byteValu: dependent variable
	def _gfPolyEval(self, argPoly, argX):
		# initialise the polynomial result
		byteValu = argPoly[0]
		
		# evaluate the polynomial argument
		for polyPos in range(1, len(argPoly)):
			tempValu = self.__gfMult(byteValu, argX) 
			tempValu = tempValu ^ argPoly[polyPos]
			byteValu = tempValu
		return (byteValu)
	
	## REED-SOLOMON SUPPORT ROUTINES
	# -----
	# Prepare the generator polynomial
	# errSize: number of error symbols
	# polyValu: generator polynomial
	def _rsGenPoly(self, errSize):
		polyValu = [1]
		
		for polyPos in range(0, errSize):
			tempVal = [1, self.__GFEXP[polyPos]]
			polyValu = self._gfPolyMult(polyValu, tempVal)
		return (polyValu)
	
	## REED-SOLOMON ENCODING
	# ------
	# argMesg: the message block
	# errSize: number of error symbols
	# outBuffer: the encoded output buffer
	def RSEncode(self, argMesg, errSize):
		# prepare the generator polynomial
		polyGen = self._rsGenPoly(errSize)
		
		# prepare the output buffer
		outBuffer = (len(argMesg) + errSize)
		outBuffer = [0] * outBuffer
		
		# initialise the output buffer
		for mesgPos in range(0, len(argMesg)):
			mesgChar = argMesg[mesgPos]
			outBuffer[mesgPos] = ord(mesgChar)
		
		# begin encoding
		for mesgPos in range(0, len(argMesg)):
			mesgChar = outBuffer[mesgPos]
			if (mesgChar != 0):
				for polyPos in range(0, len(polyGen)):
					tempValu = self.__gfMult(polyGen[polyPos], mesgChar)
					outBuffer[mesgPos + polyPos] ^= tempValu
		
		# finalise the output buffer
		for mesgPos in range(0, len(argMesg)):
			mesgChar = argMesg[mesgPos]
			outBuffer[mesgPos] = ord(mesgChar)
		return (outBuffer)
	
	## REED-SOLOMON DECODING
	# -----
	# Generate the syndrome polynomial
	# argCode: the code block
	# errSize: number of error symbols
	# polyValu: the syndrome polynomial
	def _rsSyndPoly(self, argCode, errSize):
		polyValu = [0] * errSize
		
		# compute the polynomial terms
		for errPos in range(0, errSize):
			byteValu = self.__GFEXP[errPos] 
			polyValu[errPos] = self._gfPolyEval(argCode, byteValu)
		return (polyValu)
	
	# The Forney algorithm
	# polySynd: the syndrome polynomial
	# eraseLoci: list of erasures
	# errSize: number of error symbols
	# polyValu: the error locator polynomial 
	def _rsForney(self, polySynd, eraseLoci, errSize):
		# make a copy of the syndrome polynomial
		polyValu = list(polySynd)
		
		# compute the polynomial terms
		for posI in range(0, len(eraseLoci)):
			termX = errSize - 1 - eraseLoci[posI]
			termX = self.__GFEXP[termX]
			for posJ in range(0, len(polyValu) - 1):
				termY = self.__gfMult(polyValu[posJ], termX)
				termY ^= polyValu[posJ + 1]
				polyValu[posJ] = termY
			polyValu.pop()
		return (polyValu)
	
	# Locate the message errors
	# errLoci: error locator polynomial
	# errSize: number of error symbols
	def _rsFindErr(self, errLoci, errSize):
		errPoly = [1]
		tempPoly = [1]
		
		# generate the error locator polynomial
		# - Berklekamp-Massey algorithm
		for posSynd in range(0, len(errLoci)):
			tempPoly.append(0)
			termSynd = errLoci[posSynd]
			
			for posErr in range(1, len(errPoly)):
				termPoly = errPoly[len(errPoly) - posErr - 1]
				termPoly = self.__gfMult(termPoly, errLoci[posSynd - posErr])
				termSynd ^= termPoly
			
			if (termSynd != 0):
				if (len(tempPoly) > len(errPoly)):
					tNewP = self._gfPolyScale(tempPoly, termSynd)
					tempPoly = self._gfPolyScale(errPoly, self.__gfDivi(1, termSynd))
					errPoly = tNewP
				
				tempValu = self._gfPolyScale(tempPoly, termSynd)
				errPoly = self._gfPolyAdd(errPoly, tempValu)
		
		# count the number of errors
		errCount = len(errPoly) - 1
		if ((errCount * 2) > len(errLoci)):
			print ("Too many errors to correct")
			return (None)
		else:
			print ("Error count: ", errCount, len(errLoci))
		
		# calculate the polynomial zeroes
		errList = []
		for errPos in range(0, errSize):
			errZed = self._gfPolyEval(errPoly, self.__GFEXP[255 - errPos])
			if (errZed == 0):
				errZed = errSize - errPos - 1
				errList.append(errZed)
		
		if (len(errList) != errCount):
			print ("Could not locate the errors")
			return (None)
		else:
			return (errList)
	
	# Correct errors and erasures
	# argCode: the message code block
	# polySynd: the sydrome polynomial
	# errList: list of error and erasure positions
	def _rsCorrect(self, argCode, polySynd, errList):
		# prepare the locator polynomial
		polyLoci = [1]
		for errPos in range(0, len(errList)):
			errTerm = len(argCode) - errList[errPos] - 1
			errTerm = self.__GFEXP[errTerm]
			polyLoci = self._gfPolyMult(polyLoci, [errTerm, 1])
		
		# prepare the error evaluator polynomial
		errEval = polySynd[0:len(errList)]
		errEval.reverse()
		errEval = self._gfPolyMult(errEval, polyLoci)
		
		tMark = len(errEval) - len(errList)
		errEval = errEval[tMark:len(errEval)]
		
		# the error locator polynomial, minus even terms
		errLoci = polyLoci[len(polyLoci) % 1 : len(polyLoci) : 2]
		
		# start correcting
		for errPos in range(0, len(errList)):
			errByte = errList[errPos] - len(argCode) + 256
			errByte = self.__GFEXP[errByte]
			
			errValu = self._gfPolyEval(errEval, errByte)
			
			errAdj = self.__gfMult(errByte, errByte)
			errAdj = self._gfPolyEval(errLoci, errAdj)
			
			mesgByte = self.__gfMult(errByte, errAdj)
			mesgByte = self.__gfDivi(errValu, mesgByte)
			argCode[errList[errPos]] ^= mesgByte
		return (argCode)
	
	# Main decode routine
	# argCode: the message code block
	# errSize: number of error symbols
	def RSDecode(self, argCode, errSize):
		codeBuffer = list(argCode)
		eraseCount = [codePos for codePos, value in enumerate(codeBuffer) if value < 0]
        
		if len(eraseCount) > errSize:
			print("Too many erasures")
			return None
        
		polySynd = self._rsSyndPoly(codeBuffer, errSize)
		if max(polySynd) == 0:
			return codeBuffer

		errLoci = self._rsForney(polySynd, eraseCount, len(codeBuffer))
		errList = self._rsFindErr(errLoci, len(codeBuffer))
		if errList is None:
			print("Could not find any errors")
			return None
		else:
			print("Located errors:", errList)

		outMesg = self._rsCorrect(codeBuffer, polySynd, eraseCount + errList)
		return outMesg