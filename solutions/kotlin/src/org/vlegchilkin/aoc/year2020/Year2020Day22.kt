package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toPair
import org.vlegchilkin.aoc.toList
import java.util.LinkedList

class Year2020Day22(input: String) : Solution {
  private val cards = input.toList("\n\n") { player ->
    player.split('\n').drop(1).map { it.toInt() }
  }

  private fun score(players: Pair<List<Int>, List<Int>>): Int {
    val deck = players.first.ifEmpty { players.second }
    return deck.foldRightIndexed(0) { i, value, result -> result + (deck.size - i) * value }
  }

  override fun partA(): Any {
    val (first, second) = cards.map { LinkedList(it) }
    while (first.isNotEmpty() && second.isNotEmpty()) {
      (first.pop() to second.pop()).also { (f, s) ->
        if (f > s) {
          first.add(f)
          first.add(s)
        }
        else {
          second.add(s)
          second.add(f)
        }
      }
    }
    return score(first to second)
  }

  override fun partB(): Any {
    fun recursiveCombat(players: Pair<List<Int>, List<Int>>): Pair<Boolean, Pair<List<Int>, List<Int>>?> {
      val (first, second) = LinkedList(players.first) to LinkedList(players.second)
      val cache = mutableSetOf<String>()
      while (first.isNotEmpty() && second.isNotEmpty()) {
        if (!cache.add(first.joinToString(",")) || !cache.add(second.joinToString(","))) {
          return true to null
        }
        val f = first.pop()
        val s = second.pop()
        val winner = if (f <= first.size && s <= second.size) {
          recursiveCombat(first.take(f) to second.take(s)).first
        }
        else {
          f > s
        }
        if (winner) {
          first.add(f)
          first.add(s)
        }
        else {
          second.add(s)
          second.add(f)
        }
      }
      return first.isNotEmpty() to (first to second)
    }

    val finalDeck = recursiveCombat(cards.toPair()).second!!
    return score(finalDeck)
  }

  companion object : Test(2020, 22, { Year2020Day22(it) })
}