default rel

extern ExitProcess
extern MessageBoxA

global main

section .data
title db "REDEEM", 0
text db "D'you wannt to redeem $1000k?", 0
tet3 db "ACESSING FILES...", 0
text2 db "--Your computer has been hacked---", 0
hacke db "-WINDOWS SECURITY-", 0
haceT db "-/Warning\-Your system has been hacked", 0
text2T db "HAHAHA", 0
text1 db "FINE", 0
text1T db "NO REDEEM HAPPENED"

section .text
main:
    sub rsp, 40

    mov rcx, 0
    lea rdx, [text]
    lea r8, [title]
    mov r9d, 65
    call MessageBoxA

    cmp rax, 1
    jne no_hack
    je HAK

    no_hack:
        mov rcx, 0
        lea rdx, [text1]
        lea r8, [text1T]
        mov r9, 16

        call MessageBoxA
        jmp end
    
    HAK:
        mov rcx, 0
        lea rdx, [text2]
        lea r8, [tet3]
        mov r9, 0

        call MessageBoxA
        jmp hacked

        hacked:
            mov rcx, 0
            lea rdx, [hacke]
            lea r8, [haceT]
            mov r9, 48

            call MessageBoxA
            jmp cros

    cros:
        jmp end


    end:
        mov rcx, 0
        call ExitProcess