package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/19: Aplenty
 */
class Year2023Day19(input: String) : Solution {
  private val workflows: Map<String, Workflow>
  private val parts: List<Map<Char, Int>>

  data class Rule(val field: Char, val sign: Char, val value: Int, val action: String)
  data class Workflow(val rules: List<Rule>, val defaultAction: String)

  init {
    val (wfData, pData) = input.toList("\n\n") { it.split("\n") }
    workflows = wfData.associate { d ->
      val name = d.substringBefore("{")
      val groups = d.removeSurrounding("$name{", "}").split(',')
      val rules = groups.dropLast(1).map { r ->
        val (a, b) = r.split(':')
        Rule(a[0], a[1], a.substring(2).toInt(), b)
      }
      name to Workflow(rules, groups.last())
    }
    parts = pData.map { d ->
      d.removeSurrounding("{", "}").split(',').associate {
        val (a, b) = it.split('=')
        a[0] to b.toInt()
      }
    }
  }

  private fun dfs(action: String, available: Map<Char, IntRange>): Long {
    if (available.values.any { it.isEmpty() }) return 0L
    when (action) {
      "R" -> return 0L
      "A" -> return available.values.fold(1L) { acc, c -> acc * (c.last - c.first + 1) }
    }
    val workflow = workflows[action]!!
    val ranges = available.toMutableMap()

    var result = 0L
    for (rule in workflow.rules) {
      val range = ranges[rule.field]!!
      val (take, remains) = when (rule.sign) {
        '<' -> range.first..minOf(rule.value - 1, range.last) to rule.value..range.last
        '>' -> maxOf(rule.value + 1, range.first)..range.last to range.first..rule.value
        else -> error("Illegal sign")
      }
      if (!take.isEmpty()) {
        ranges[rule.field] = take
        result += dfs(rule.action, ranges)
        ranges[rule.field] = remains
      }
    }
    result += dfs(workflow.defaultAction, ranges)
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
