import csv, os, subprocess, StringIO, numpy, sys

pwd = os.getcwd()
for number in range(int(sys.argv[1]),int(sys.argv[2])):
        projectPath = "/share/ProjectData/Math/"+`number`
        finalResult = "/share/TestPrioritization/test-coverage/result"+"/final_"+`number`+".csv"

	#projectPath = "/home/sajad/workspace/commons-math"
	#finalResult = "/home/sajad/workspace/commons-math/final.csv"
        reportPath = projectPath+"/report.csv"

        testFinderCommand = "bash "+pwd+"/TestFinder_release/run_testfinder.sh "+projectPath+" org.apache.commons.math3"
        testMethods = subprocess.check_output(testFinderCommand, shell=True)
        s = StringIO.StringIO(testMethods)
        numberOfAllTest = 0
        numberOfFailedTest = 0
        numberOfRowOfCsvFile = 0

        for test in s:
                indexOfSharp = test.index('#')
		if test.startswith("org.apache.commons.math3.random.SynchronizedRandomGeneratorTest#testMath899Sync", 0) :
					continue
                if test.endswith("AbstractTest", 0,indexOfSharp):
					continue
                numberOfAllTest+=1

                if numberOfAllTest == 1:
                        jacocoCommand = "java -javaagent:"+pwd+"/jacoco/lib/jacocoagent.jar=destfile="+projectPath+"/jacoco.exec -cp .:"+pwd+"/runSingleTestWithJunit/classes/:"+projectPath+"/target/classes/:"+projectPath+"/target/test-classes/:/usr/share/java/junit-4.8.2.jar SingleJUnitTestRunner "+test
                        output = subprocess.check_output(jacocoCommand, shell=True)
                        if output == "true":
                                numberOfFailedTest+=1
                        reportBuilderCommand = "java -jar "+pwd+"/JacocoReportBuilder_relase/JacocoReportBuilder-1.0.0.jar "+projectPath
                        output = subprocess.check_output(reportBuilderCommand, shell=True)
                        print output
                        removeJacocoCommand = "rm "+projectPath+"/jacoco.exec"
                        output = subprocess.check_output(removeJacocoCommand, shell=True)
                        print output
                        with open(reportPath, "rb") as f:
                                reader=csv.reader(f,delimiter=',')
                                x=list(reader)
                                tmpResult=numpy.array(x).astype('string')
                                numberOfRowOfCsvFile = tmpResult.shape[0]
                        output = subprocess.check_output("rm "+reportPath, shell=True)


        result = numpy.empty(shape=(numberOfRowOfCsvFile,numberOfAllTest), dtype=object)
        print result.shape

        s = StringIO.StringIO(testMethods)
        i=0
        for test in s:
                print "test="+test
                indexOfSharp = test.index('#')
		if test.startswith("org.apache.commons.math3.random.SynchronizedRandomGeneratorTest#testMath899Sync", 0) :
					continue
                if test.endswith("AbstractTest", 0,indexOfSharp):
                        continue
                jacocoCommand = "java -javaagent:"+pwd+"/jacoco/lib/jacocoagent.jar=destfile="+projectPath+"/jacoco.exec -cp .:"+pwd+"/runSingleTestWithJunit/classes/:"+projectPath+"/target/classes/:"+projectPath+"/target/test-classes/:/usr/share/java/junit-4.8.2.jar SingleJUnitTestRunner "+test
                output = subprocess.check_output(jacocoCommand, shell=True)
                if output == "true":
                        numberOfFailedTest+=1
                reportBuilderCommand = "java -jar "+pwd+"/JacocoReportBuilder_relase/JacocoReportBuilder-1.0.0.jar "+projectPath
                output = subprocess.check_output(reportBuilderCommand, shell=True)
                print output
                removeJacocoCommand = "rm "+projectPath+"/jacoco.exec"
                output = subprocess.check_output(removeJacocoCommand, shell=True)
                print output

                i+=1
                if i == 1:
                        result[0][0]="methodName/testName"
                        with open(reportPath) as f:
                                readerOfCsv = csv.reader(f, delimiter=',')
                                next(readerOfCsv, None)
                                j=1
                                for row in readerOfCsv:
                                        result[j][0]=row[0]
                                        j+=1

                with open(reportPath) as f:
                        reader = csv.reader(f, delimiter=',')
                        next(reader, None)
                        result[0][i]=test[:-1]
                        j=1
                        for row in reader:
                                result[j][i]=row[1]
                                j+=1

                removeCommand = "rm "+reportPath
                output = subprocess.check_output(removeCommand, shell=True)
                print output

                print i

#       print result

        numpy.savetxt(finalResult, result, delimiter=",",  fmt="%s")

        print "number of failed test methods="
        print numberOfFailedTest
        print "total number of test methods="
        print numberOfAllTest


