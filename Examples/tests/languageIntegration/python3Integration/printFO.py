print("""
functions {
    pythonDynamicOutput
    {
        type python3Integration;

        startCode "print('Dynamic Starting')";
        executeCode "print('Dynamic Executing')";
        endCode "print('Never been here')";
        //        tolerateExceptions true;
        parallelMasterOnly true;
        useNumpy false;
        useIPython false;
    }
    pythonDynamicOutput2
    {
         $pythonDynamicOutput;
         parallelMasterOnly false;
         isParallelized true;
    }
}
""")
