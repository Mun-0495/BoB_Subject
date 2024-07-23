package org.example

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class   E2EKeypadApplication {
    fun main(args: Array<String>) {
        runApplication<E2EKeypadApplication>(*args)
    }
}