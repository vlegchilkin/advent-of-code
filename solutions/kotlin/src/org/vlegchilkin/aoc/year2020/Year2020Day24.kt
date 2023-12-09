package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*
import kotlin.collections.ArrayDeque

class Year2020Day24(input: String) : Solution {
  private val lines = input.toList { it }
  override fun partAB(): Pair<Int, Int> {
    fun parse(value: String): Pair<Int, Int> {
      var pos = 0 to 0
      val buffer = ArrayDeque(value.toList())
      while (buffer.isNotEmpty()) {
        val side = buffer.removeFirst().let { if (it == 'e' || it == 'w') "$it" else "$it${buffer.removeFirst()}" }
        pos += HEXAGONAL[side]!!
      }
      return pos
    }

    val tiles = lines.map { parse(it) }
    val black = mutableSetOf<Pair<Int, Int>>()
    tiles.forEach {
      if (it in black) {
        black.remove(it)
      }
      else {
        black.add(it)
      }
    }
    val partA = black.size

    fun swap(floor: Set<Pair<Int, Int>>): Set<Pair<Int, Int>> {
      val possibles = floor.map { zero -> HEXAGONAL.values.map { zero + it } }.flatten().toMutableSet()
      possibles.addAll(floor)
      return possibles.filter { zero ->
        val neighbours = HEXAGONAL.values.map { zero + it }.count { it in floor }
        (neighbours == 2) || (neighbours == 1 && zero in floor)
      }.toSet()
    }

    var floor: Set<Pair<Int, Int>> = black
    repeat(100) {
      floor = swap(floor)
    }
    val partB = floor.size

    return partA to partB
  }


  companion object : Test(2020, 24, { Year2020Day24(it) }) {
    val HEXAGONAL = mapOf(
      "e" to (1 to 1),
      "w" to (-1 to -1),
      "sw" to (-1 to 0),
      "se" to (0 to 1),
      "nw" to (0 to -1),
      "ne" to (1 to 0),
    )
  }
}