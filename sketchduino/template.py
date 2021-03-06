# -*- coding: utf-8 -*-
'''
Copyright 2012 Rodrigo Pinheiro Matias <rodrigopmatias@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

templates = {
    'static_link': '''
\t@$(AR) rcs %(lib)s %(obj)s
\t@echo " [\033[33m\033[1mAR\033[0m]      - \033[37m\033[1m%(obj)s\033[0m to \033[37m\033[1m%(lib)s\033[0m"''',
    'c_obj_ruler': '''%(obj)s: %(source)s
\t@$(CC) $(CFLAGS) $(INCLUDE) -c %(source)s -o %(obj)s 1>> compile.log 2>> compile.err
\t@echo " [\033[33m\033[1mCC\033[0m]      - \033[37m\033[1m%(source)s\033[0m"''',
    'asm_obj_ruler': '''%(obj)s: %(source)s
\t@$(AS) $(ASFLAGS) -o %(obj)s %(source)s 1>> compile.log 2>> compile.err
\t@echo " [\033[33m\033[1mAS\033[0m]      - \033[37m\033[1m%(source)s\033[0m"''',
    'c_asm_ruler': '''%(obj)s: %(source)s
\t@$(CC) $(CFLAGS) $(INCLUDE) -c %(source)s -S -o %(obj)s 1>> compile.log 2>> compile.err
\t@echo " [\033[33m\033[1mCC\033[0m]      - \033[37m\033[1m%(source)s\033[0m"''',
    'cxx_obj_ruler': '''%(obj)s: %(source)s
\t@$(CXX) $(CXXFLAGS) $(INCLUDE) -c %(source)s -o %(obj)s 1>> compile.log 2>> compile.err
\t@echo " [\033[33m\033[1mCXX\033[0m]     - \033[37m\033[1m%(source)s\033[0m"''',
    'cxx_asm_ruler': '''%(obj)s: %(source)s
\t@$(CXX) $(CXXFLAGS) $(INCLUDE) -c %(source)s -S -o %(obj)s 1>> compile.log 2>> compile.err
\t@echo " [\033[33m\033[1mCXX\033[0m]     - \033[37m\033[1m%(source)s\033[0m"''',
    'avr-main.cc': '''/**
 * Generated with sketch %(version)s
 **/
#include <avr/sleep.h>

int main(void) {
    for(;;)
        sleep_mode();

    return 0;
}''',
    'main.cc': '''/**
 * Generated with sketch %(version)s
 **/
#include <Arduino.h>

/**
 * Setup of the firmware
 **/
void setup() {
}

/**
 * Schedule events for firmware program
 **/
void loop() {
    delay(250);
}''',
    'Makefile': '''##########################################
# Makefile generated with sketch %(version)s
##########################################

# Defines of Arduino
ARDUINO_HOME=%(sdk_home)s
ARDUINO_CORE=$(ARDUINO_HOME)/hardware/arduino/cores
ARDUINO_VARIANT=$(ARDUINO_HOME)/hardware/arduino/variants/%(variant)s

# Define toolchain
CC=%(cc)s
CXX=%(cxx)s
AS=%(asm)s
LD=%(ld)s
AR=%(ar)s
OBJCOPY=%(objcopy)s
SIZE=%(size)s
AVRDUDE=%(avrdude)s
PROGRAMER=%(programer)s
LIB=
INCLUDE=-I$(ARDUINO_CORE)/arduino -I$(ARDUINO_VARIANT) -I$(ARDUINO_CORE) -I lib/

#Define of MCU
MCU=%(mcu)s
CLOCK=%(clock_hz)sUL
ARDUINO=%(sdk_version)s

# Define compiler flags
_CFLAGS=-Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=$(MCU) \\
          -DF_CPU=$(CLOCK) -MMD -DARDUINO=$(ARDUINO) \\
          -fpermissive -lm -Wl,-u,vfprintf -lprintf_min
CFLAGS=$(_CFLAGS) -std=c99
CXXFLAGS=$(_CFLAGS) -std=c++98
ASFLAGS=-mmcu $(MCU)

# Define compiler rulers
OBJ=%(obj_dep)s
CORE_OBJ=%(core_obj_dep)s
AOUT=binary/%(project_name)s-%(mcu)s.elf
HEX=binary/%(project_name)s-%(mcu)s.hex
EPP=binary/%(project_name)s-%(mcu)s.epp
CORE_LIB=binary/core.a
LIB_DEPS=%(lib_deps)s
LD_FLAGS=-Os -Wl,--gc-sections -mmcu=$(MCU) -lm

AVRDUDE_OPTIONS = -p$(MCU) -c$(PROGRAMER) %(pgrextra)s -Uflash:w:$(HEX):i

SIZE_OPTS=-C --mcu=$(MCU)

CONFIG_EXISTS=$(shell [ -e "Makefile.config" ] && echo 1 || echo 0)

ifeq ($(CONFIG_EXISTS), 1)
  include Makefile.config
endif

all: $(HEX) $(EPP)

rebuild: clean all

deploy: $(HEX)
\t$(AVRDUDE) $(AVRDUDE_OPTIONS)

$(HEX): $(EPP)
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] - \033[37m\033[1mFirmware\033[0m"
\t@$(OBJCOPY) -O ihex -R .eeprom $(AOUT) $(HEX)

$(EPP): $(AOUT)
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] - \033[37m\033[1mMemory of EEPROM\033[0m"
\t@$(OBJCOPY) -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 $(AOUT) $(EPP)

size: $(AOUT)
\t@$(SIZE) $(SIZE_OPTS) $(AOUT)

$(AOUT): clear-compiler $(OBJ) $(CORE_LIB) $(LIB_DEPS)
\t@echo " [\033[33m\033[1mLD\033[0m]      - \033[37m\033[1m$(AOUT)\033[0m"
\t@$(CXX) $(LD_FLAGS) $(LIB) $(OBJ) $(CORE_LIB) $(LIB_DEPS) -o $(AOUT)

$(CORE_LIB): $(CORE_OBJ)%(core_ruler)s

%(asm_rulers)s

%(obj_rulers)s

%(libs_rulers)s

%(core_asm_rulers)s

%(core_obj_rulers)s

clear-compiler:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear compiler logs"
\trm -f compile.*

clean-tmp:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear temporary files"
\t@rm -f tmp/*

clean-bin:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear binary files"
\t@rm -f binary/*

clean:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear temporary files"
\t@rm -f tmp/*
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear binary files"
\t@rm -f binary/*
''',
    'avr-Makefile': '''##########################################
# Makefile generated with sketch %(version)s
##########################################

# Define toolchain
CC=%(cc)s
CXX=%(cxx)s
AS=%(asm)s
LD=%(ld)s
AR=%(ar)s
OBJCOPY=%(objcopy)s
SIZE=%(size)s
AVRDUDE=%(avrdude)s
PROGRAMER=%(programer)s
LIB=
INCLUDE=-I lib/

#Define of MCU
MCU=%(mcu)s
CLOCK=%(clock_hz)sUL

# Define compiler flags
_CFLAGS=-Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=$(MCU) \\
          -DF_CPU=$(CLOCK) -fpermissive -lm -Wl,-u,vfprintf -lprintf_min
CFLAGS=$(_CFLAGS) -std=c99
CXXFLAGS=$(_CFLAGS) -std=c++98
ASFLAGS=-mmcu $(MCU)

# Define compiler rulers
ASM=%(asm_dep)s
OBJ=%(obj_dep)s
LIB_DEPS=%(lib_deps)s
AOUT=binary/%(project_name)s-%(mcu)s.elf
HEX=binary/%(project_name)s-%(mcu)s.hex
EPP=binary/%(project_name)s-%(mcu)s.epp
LD_FLAGS=-Os -Wl,--gc-sections -mmcu=$(MCU) -lm

AVRDUDE_OPTIONS = -p$(MCU) -c$(PROGRAMER) %(pgrextra)s -Uflash:w:$(HEX):i

SIZE_OPTS=-A

CONFIG_EXISTS=$(shell [ -e "Makefile.config" ] && echo 1 || echo 0)

ifeq ($(CONFIG_EXISTS), 1)
  include Makefile.config
endif

all: $(HEX) $(EPP)

rebuild: clean all

deploy: $(HEX)
\t$(AVRDUDE) $(AVRDUDE_OPTIONS)

$(HEX): $(EPP)
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] - \033[37m\033[1mFirmware\033[0m"
\t@$(OBJCOPY) -O ihex -R .eeprom $(AOUT) $(HEX)

$(EPP): $(AOUT)
\t@echo " [\033[33m\033[1mOBJCOPY\033[0m] - \033[37m\033[1mMemory of EEPROM\033[0m"
\t@$(OBJCOPY) -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 $(AOUT) $(EPP)

size: $(AOUT)
\t@$(SIZE) $(SIZE_OPTS) $(AOUT)

$(AOUT): clear-compiler $(OBJ) $(LIB_DEPS)
\t@echo " [\033[33m\033[1mLD\033[0m]      - \033[37m\033[1m$(AOUT)\033[0m"
\t@$(CXX) $(LD_FLAGS) $(LIB) $(OBJ) $(LIB_DEPS) -o $(AOUT)

%(asm_rulers)s

%(obj_rulers)s

%(libs_rulers)s

clear-compiler:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear compiler logs"
\t@rm -f compile.*

clean-tmp:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear temporary files"
\t@rm -f tmp/*

clean-bin:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear binary files"
\t@rm -f binary/*

clean:
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear temporary files"
\t@rm -f tmp/*
\t@echo " [\033[33m\033[1mRM\033[0m]      - Clear binary files"
\t@rm -f binary/*
'''
}
