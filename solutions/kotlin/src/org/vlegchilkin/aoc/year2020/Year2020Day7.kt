package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import java.util.LinkedList

class Year2020Day7(input: String) : Solution {
  private val rules = input.trim().split("\n").associate { rule ->
    val (_, bag, innerBags) = PATTERN_WRAPPER.matchEntire(rule)!!.groupValues
    bag to PATTERN_INNER_BAGS.findAll(innerBags).map { it.groupValues }.map { it[1].toInt() to it[2] }.toList()
  }


  override fun partA(): Any {
    val parents = mutableMapOf<String, MutableSet<String>>()
    rules.forEach { (bag, inners) ->
      inners.forEach {
        parents.getOrPut(it.second) { mutableSetOf() }.add(bag)
      }
    }

    val queue = LinkedList<String>()
    queue.offer(MY_BAG)
    val visited = mutableSetOf(queue.first)
    while (queue.isNotEmpty()) {
      val bag = queue.pop()
      parents[bag]?.forEach {
        if (it !in visited) {
          visited.add(it)
          queue.offer(it)
        }
      }
    }
    return visited.size - 1
  }

  override fun partB(): Any {
    val cache = mutableMapOf<String, Int>()

    fun dfs(bag: String): Int {
      return cache.getOrPut(bag) { 1 + (rules[bag]?.sumOf { it.first * dfs(it.second) } ?: 0) }
    }

    return dfs(MY_BAG) - 1
  }

  companion object : Test(2020, 7, { Year2020Day7(it) }) {
    const val MY_BAG = "shiny gold"
    val PATTERN_WRAPPER = """^(\w+ \w+) bags contain (.*)$""".toRegex()
    val PATTERN_INNER_BAGS = """(\d+) (\w+ \w+) bags?[,.]""".toRegex()
  }
}