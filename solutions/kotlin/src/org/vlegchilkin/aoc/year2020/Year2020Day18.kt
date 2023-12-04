package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toList
import java.util.LinkedList

class Year2020Day18(input: String) : Solution {
  private val expressions = input.toList { it }

  private fun eval(expr: String, plusPriority: Boolean = false): Long {
    val arg = LinkedList<Long>()
    val op = LinkedList<Char>()
    var num: Long? = null

    "($expr)".filter { it != ' ' }.forEach { c ->
      if (c.isDigit()) {
        num = (num ?: 0) * 10 + (c - '0')
        return@forEach
      }
      num?.let {
        arg.push(num)
        num = null
      }

      if (c != '(') {
        when (op.peek()) {
          '+' -> {
            arg.push(arg.pop() + arg.pop())
            op.pop()
          }
          '*' -> if (!plusPriority) {
            arg.push(arg.pop() * arg.pop())
            op.pop()
          }
        }
      }

      if (c == ')') {
        while (op.pop() != '(') {
          arg.push(arg.pop() * arg.pop())
        }
      }
      else op.push(c)
    }

    return arg.pop()
  }

  override fun partA(): Long {
    return expressions.sumOf { eval(it) }
  }

  override fun partB(): Long {
    return expressions.sumOf { eval(it, plusPriority = true) }
  }

  companion object : Test(2020, 18, { Year2020Day18(it) })
}