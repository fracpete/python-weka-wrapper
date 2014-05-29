Troubleshooting
===============

Mac OSX
-------

* **Q:** Why does javabridge fail with compiler error `clang: error: unknown argument: '-mno-fused-madd'`?

  **A:** XCode 5.1 changed how unknown arguments are handled and now treats them  as error (`source <http://bruteforce.gr/bypassing-clang-error-unknown-argument.html>`_). You can precede the `pip install javabridge` command with the following environment variable:

  .. code-block:: bash

     ARCHFLAGS="-Wno-error=unused-command-line-argument-hard-error-in-future" pip install javabridge

* **Q:** Compiling javabridge fails with missing `jni.h` header file - what now?

  **A:** You will need an Oracle JDK installed for this. `Download <http://www.oracle.com/technetwork/java/javase/downloads/>`_ and install one. Below is a command-line that uses the `jni.h` header file that comes with `1.7.0_45`:

  .. code-block:: bash

     ARCHFLAGS="-I/Library/Java/JavaVirtualMachines/jdk1.7.0_45.jdk/Contents/Home/include/ -I/Library/Java/JavaVirtualMachines/jdk1.7.0_45.jdk/Contents/Home/include/darwin" pip install --user javabridge

  *PS:* You may need to combine the `ARCHFLAGS` setting with the one from the previous Q&A.

* **Q:** When I use `import javabridge` in my Python shell, a
  dialog pops up, telling me that I don't have Java installed. However, I have
  an Oracle JDK installed. What's wrong?

  **A:** Java environments that are not from Apple don't seem to get picked up
  by Python correctly. Simply install the Java 1.6 that Apple supplies on your
  system as well.


