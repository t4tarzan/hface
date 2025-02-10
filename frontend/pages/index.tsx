import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Text,
  useColorModeValue,
} from '@chakra-ui/react'
import Head from 'next/head'

export default function Home() {
  return (
    <>
      <Head>
        <title>AI Tools Platform</title>
        <meta name="description" content="AI Tools Platform powered by Hugging Face" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Box as="main" minH="100vh" bg={useColorModeValue('gray.50', 'gray.900')}>
        <Container maxW="container.xl" py={10}>
          <Heading as="h1" mb={8} textAlign="center">
            AI Tools Platform
          </Heading>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={8}>
            {/* Tool cards will be mapped here */}
            <Box
              p={6}
              bg={useColorModeValue('white', 'gray.800')}
              rounded="lg"
              shadow="base"
              transition="all 0.2s"
              _hover={{ shadow: 'lg' }}
            >
              <Heading as="h3" size="md" mb={2}>
                Coming Soon
              </Heading>
              <Text color={useColorModeValue('gray.600', 'gray.300')}>
                AI tools will be available here soon.
              </Text>
            </Box>
          </SimpleGrid>
        </Container>
      </Box>
    </>
  )
}
