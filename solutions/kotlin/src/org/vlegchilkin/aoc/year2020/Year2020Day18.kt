package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toList

class Year2020Day18(input: String) : Solution {
  private val expressions = input.toList { it }

  private fun eval(expr: String, plusPriority: Boolean = false): Long {
    val arg = ArrayDeque<Long>()
    val op = ArrayDeque<Char>()
    var num: Long? = null

    "($expr)".filter { it != ' ' }.forEach { c ->
      if (c.isDigit()) {
        num = (num ?: 0) * 10 + (c - '0')
        return@forEach
      }
      num?.let {
        arg.addFirst(it)
        num = null
      }

      if (c != '(') {
        when (op.first()) {
          '+' -> {
            arg.addFirst(arg.removeFirst() + arg.removeFirst())
            op.removeFirst()
          }
          '*' -> if (!plusPriority) {
            arg.addFirst(arg.removeFirst() * arg.removeFirst())
            op.removeFirst()
          }
        }
      }

      if (c == ')') {
        while (op.removeFirst() != '(') {
          arg.addFirst(arg.removeFirst() * arg.removeFirst())
        }
      }
      else op.addFirst(c)
    }

    return arg.removeFirst()
  }

  override fun partA(): Long {
    return expressions.sumOf { eval(it) }
  }

  override fun partB(): Long {
    return expressions.sumOf { eval(it, plusPriority = true) }
  }

  companion object : Test(2020, 18, { Year2020Day18(it) })
}