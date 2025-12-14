package org.vlegchilkin.aoc.year2025

import org.vlegchilkin.aoc.*
import kotlin.collections.component1
import kotlin.collections.forEach
import kotlin.collections.sumOf


/**
 * 2025/11: Reactor
 */
class Year2025Day11(input: String) : Solution {
  private val graph: Graph<String> = input.toList { line ->
    val node = line.substringBefore(": ")
    val links = line.substringAfter(": ").split(' ')
    node to links
  }.toMap()

  private val reversed = graph.values.flatten().distinct().associateWith { mutableSetOf<String>() }

  init {
    graph.forEach { (from, to) ->
      to.forEach { reversed[it]!!.add(from) }
    }
  }

  private fun find(from: String, to: String): Long {
    val cache = mutableMapOf(from to 1L)

    fun recu(node: String): Long {
      cache[node]?.let { return it }
      val result = reversed[node]?.sumOf { recu(it) } ?: 0
      cache[node] = result
      return result
    }
    return recu(to)
  }

  override fun partA(): Any {
    return find("you", "out")
  }

  override fun partB(): Any {
    val p1 = find("svr", "fft") * find("fft", "dac") * find("dac", "out")
    val p2 = find("svr", "dac") * find("dac", "fft") * find("fft", "out")
    return p1 + p2
  }

  companion object : Test(2025, 11, { Year2025Day11(it) })
}
