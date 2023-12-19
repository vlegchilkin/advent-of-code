package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/19: Aplenty
 */
class Year2023Day19(input: String) : Solution {
  private val workflows: Map<String, List<Rule>>
  private val parts: List<Map<Char, Int>>

  data class Rule(val field: Char? = null, val sign: Char? = null, val value: Int? = null, val action: String)

  init {
    val (wfData, pData) = input.toList("\n\n") { it.split("\n") }
    workflows = wfData.associate { d ->
      val name = d.substringBefore("{")
      val groups = d.removeSurrounding("$name{", "}").split(',')
      val rules = groups.map { r ->
        if (r.contains(":")) {
          val (a, b) = r.split(':')
          Rule(a[0], a[1], a.substring(2).toInt(), b)
        }
        else {
          Rule(action = r)
        }
      }
      name to rules
    }
    parts = pData.map { d ->
      d.removeSurrounding("{", "}").split(',').associate {
        val (a, b) = it.split('=')
        a[0] to b.toInt()
      }
    }
  }

  private fun dfs(action: String, ranges: Map<Char, IntRange>): Long {
    when (action) {
      "R" -> return 0L
      "A" -> return ranges.values.fold(1L) { acc, c -> acc * (c.last - c.first + 1) }
    }

    var result = 0L
    val nonProcessed = ranges.toMutableMap()
    for (rule in workflows[action]!!) {
      if (rule.value == null) {
        result += dfs(rule.action, nonProcessed)
        break
      }
      val r = nonProcessed[rule.field!!]!!
      val (take, remains) = when (rule.sign) {
        '<' -> r.first..minOf(rule.value - 1, r.last) to rule.value..r.last
        '>' -> maxOf(rule.value + 1, r.first)..r.last to r.first..rule.value
        else -> error("Illegal sign")
      }
      if (take.isEmpty()) continue

      val dfsRanges = nonProcessed.toMutableMap().apply { replace(rule.field, take) }
      result += dfs(rule.action, dfsRanges)

      if (remains.isEmpty()) break
      nonProcessed[rule.field] = remains
    }

    return result
  }


  override fun partA(): Any {
    return parts.sumOf { part ->
      val ranges = part.mapValues { (_, v) -> v..v }
      dfs("in", ranges) * part.values.sum()
    }
  }

  override fun partB(): Any {
    return dfs("in", "xmas".associate { it to 1..4000 })
  }

  companion object : Test(2023, 19, { Year2023Day19(it) })
}
